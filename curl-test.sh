#!/bin/bash

API_URL="http://142.93.148.116:5000/api/timeline_post"

echo "Testing GET endpoint..."
curl $API_URL
echo ""

echo "Testing POST endpoint..."
curl -X POST $API_URL \
  -d "name=John Doe" \
  -d "email=john@example.com" \
  -d "content=This is a test post"
echo ""

echo "Testing GET endpoint again..."
curl $API_URL
echo ""

echo "Testing DELETE endpoint..."
curl -X DELETE $API_URL/1
echo ""