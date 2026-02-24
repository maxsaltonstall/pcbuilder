#!/bin/bash

# Configuration
DOMAIN="pcbuilder.maxsaltonstall.com"
BUCKET_NAME="$DOMAIN"
REGION="us-east-1"

echo "🚀 Deploying D&D Character Builder to S3..."

# Build the React app (without Electron)
echo "📦 Building React app..."
npm run build:react

# Create S3 bucket
echo "🪣 Creating S3 bucket..."
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>/dev/null || echo "Bucket already exists"

# Configure bucket for static website hosting
echo "🌐 Configuring static website hosting..."
aws s3 website s3://$BUCKET_NAME \
  --index-document index.html \
  --error-document index.html

# Set bucket policy for public read
echo "🔓 Setting bucket policy..."
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "PublicReadGetObject",
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::'$BUCKET_NAME'/*"
  }]
}'

# Sync built files to S3
echo "📤 Uploading files to S3..."
aws s3 sync dist/ s3://$BUCKET_NAME \
  --delete \
  --cache-control "public, max-age=31536000" \
  --exclude "index.html"

# Upload index.html with no cache (for SPA routing)
aws s3 cp dist/index.html s3://$BUCKET_NAME/index.html \
  --cache-control "public, max-age=0, must-revalidate"

echo "✅ Deployment complete!"
echo "📍 Website URL: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo ""
echo "Next steps:"
echo "1. Create CloudFront distribution for HTTPS/CDN"
echo "2. Point $DOMAIN to CloudFront in Route53"
echo "3. Request SSL certificate in ACM (us-east-1)"
