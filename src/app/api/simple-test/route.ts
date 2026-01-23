import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'OK',
    endpoint: 'simple-test',
    timestamp: new Date().toISOString(),
    message: 'Simple test endpoint working'
  });
}

export async function POST() {
  return NextResponse.json({
    status: 'OK',
    method: 'POST',
    endpoint: 'simple-test',
    timestamp: new Date().toISOString(),
    message: 'POST method working'
  });
}