#!/bin/bash

echo "🔍 Testing various endpoints for 404 errors..."
echo ""

BASE_URL="https://sales-form-chi.vercel.app"

# Test main pages
echo "Testing main pages:"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/auth/login" 
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/dashboard"

echo ""
echo "Testing API endpoints:"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/api/auth/session"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/api/auth/providers"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/api/auth/signin"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/api/debug/auth"

echo ""
echo "Testing static files:"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/favicon.ico"
curl -s -o /dev/null -w "  %{url_effective} -> %{http_code}\n" "$BASE_URL/_next/static/chunks/main.js" 2>/dev/null || echo "  Static file test failed"

echo ""
echo "🔍 Any 404 responses above indicate the problem area."