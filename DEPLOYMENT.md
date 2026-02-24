# Deployment Guide: AWS Web Hosting

## Option 1: AWS Amplify (Recommended)

### Pros:
- ✅ Automatic CI/CD from GitHub
- ✅ Free SSL certificate
- ✅ Custom domain setup in one click
- ✅ Preview deployments for PRs
- ✅ Rollback to any previous version

### Setup:
1. Push `amplify.yml` to repo (already done)
2. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
3. Click **"New app" → "Host web app"**
4. Connect GitHub → select `maxsaltonstall/pcbuilder`
5. Amplify detects settings automatically
6. Click **"Save and deploy"**
7. After first deploy, go to **"Domain management"**
8. Click **"Add domain"** → enter `maxsaltonstall.com`
9. Add subdomain: `pcbuilder.maxsaltonstall.com`
10. Amplify configures Route53 and SSL automatically

**Done!** Every `git push` triggers automatic deployment.

---

## Option 2: S3 + CloudFront + Route53

### Pros:
- ✅ Cheaper at scale ($0.50-2/month for most traffic)
- ✅ More control over caching
- ✅ Can use existing CloudFront distribution

### Setup:

#### 1. Deploy to S3
```bash
./deploy-to-s3.sh
```

#### 2. Create CloudFront Distribution
```bash
# Request SSL certificate in ACM (must be in us-east-1 for CloudFront)
aws acm request-certificate \
  --domain-name pcbuilder.maxsaltonstall.com \
  --validation-method DNS \
  --region us-east-1

# Note the CertificateArn from output
# Validate certificate by adding DNS records in Route53 (check email or console)

# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name pcbuilder.maxsaltonstall.com.s3-website-us-east-1.amazonaws.com \
  --default-root-object index.html \
  --comment "D&D Character Builder" \
  --aliases pcbuilder.maxsaltonstall.com \
  --viewer-certificate ACMCertificateArn=YOUR_CERT_ARN,SSLSupportMethod=sni-only,MinimumProtocolVersion=TLSv1.2_2021

# Or use the console: https://console.aws.amazon.com/cloudfront/
```

#### 3. Configure Route53
```bash
# Get CloudFront distribution domain (e.g., d1234abcd.cloudfront.net)
aws cloudfront list-distributions --query 'DistributionList.Items[0].DomainName'

# Create Route53 record
aws route53 change-resource-record-sets \
  --hosted-zone-id YOUR_ZONE_ID \
  --change-batch '{
    "Changes": [{
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "pcbuilder.maxsaltonstall.com",
        "Type": "A",
        "AliasTarget": {
          "HostedZoneId": "Z2FDTNDATAQYW2",
          "DNSName": "YOUR_CLOUDFRONT_DOMAIN",
          "EvaluateTargetHealth": false
        }
      }
    }]
  }'
```

---

## Code Changes Needed for Web Deployment

### Remove Electron-specific features:

**1. File System Access (Save/Load Character)**

Current code uses Electron's file system. Replace with:

```typescript
// src/services/characterStorage.ts

// BEFORE (Electron):
export async function saveCharacterToFile(character: CharacterState): Promise<void> {
  const { dialog } = require('electron').remote;
  // ... file system code
}

// AFTER (Web):
export function saveCharacterToLocalStorage(character: CharacterState): void {
  localStorage.setItem('dnd-character', JSON.stringify(character));
}

export function loadCharacterFromLocalStorage(): CharacterState | null {
  const data = localStorage.getItem('dnd-character');
  return data ? JSON.parse(data) : null;
}

// ALTERNATIVE: Download as JSON file
export function downloadCharacterAsJSON(character: CharacterState): void {
  const blob = new Blob([JSON.stringify(character, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `character-${character.concept || 'unnamed'}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
```

**2. Update package.json scripts:**

```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

**3. Update vite.config.ts (if needed):**

```typescript
export default defineConfig({
  base: '/', // or '/pcbuilder/' if hosting under subpath
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
});
```

---

## Comparison

| Feature | Amplify | S3 + CloudFront |
|---------|---------|-----------------|
| Setup Time | 10 minutes | 30 minutes |
| CI/CD | Built-in | Manual (GitHub Actions) |
| SSL | Automatic | Manual (ACM) |
| Cost (low traffic) | ~$1-2/month | ~$0.50/month |
| Cost (high traffic) | ~$5-10/month | ~$2-5/month |
| Custom domain | One click | Manual Route53 |
| Rollback | Built-in UI | Manual |
| Preview deploys | Yes | No (unless you build it) |

**Recommendation:** Start with **Amplify** for speed. Switch to S3+CloudFront later if you need cost optimization or more control.

---

## Quick Start (Amplify)

```bash
# 1. Already done: amplify.yml created
git add amplify.yml
git commit -m "Add Amplify deployment config"
git push

# 2. Go to AWS Amplify Console
# 3. Connect GitHub repo
# 4. Deploy!
```

That's it! Your app will be live at https://pcbuilder.maxsaltonstall.com
