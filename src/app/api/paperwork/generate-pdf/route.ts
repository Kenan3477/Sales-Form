import { NextRequest, NextResponse } from 'next/server';
import { getServerSession } from 'next-auth/next';
import { authOptions } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import { chromium } from 'playwright';

// ---------- Flash Team PDF Generator ----------
function escapeHtml(v: any): string {
  if (v === null || v === undefined) return "";
  return String(v)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function money(v: any): string {
  if (v === null || v === undefined || v === "") return "";
  const n = Number(v);
  if (Number.isFinite(n)) return n.toFixed(2);
  return String(v);
}

function joinAddressLines(addr: any): string {
  if (!addr) return "";
  if (Array.isArray(addr)) return addr.filter(Boolean).join("<br/>");
  return escapeHtml(addr).replace(/\n/g, "<br/>");
}

function safeFilename(s: string): string {
  return String(s || "protection-plan")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "")
    .slice(0, 80);
}

function buildHtml(data: any): string {
  const d = data || {};

  const customerName = escapeHtml(d.customerName || "");
  const email = escapeHtml(d.email || "");
  const phone = escapeHtml(d.phone || "");
  const address = joinAddressLines(d.address || "");
  const coverageStartDate = escapeHtml(d.coverageStartDate || "");
  const policyNumber = escapeHtml(d.policyNumber || "");
  const monthlyCost = d.monthlyCost !== undefined && d.monthlyCost !== null && d.monthlyCost !== ""
    ? money(d.monthlyCost)
    : "";

  const hasApplianceCover = !!d.hasApplianceCover;
  const hasBoilerCover = !!d.hasBoilerCover;

  const monthlyLine = monthlyCost
    ? `<div class="kv"><span class="k">Monthly Payment:</span> <span class="v">£${escapeHtml(monthlyCost)}</span></div>`
    : "";

  const coverLines = [
    hasApplianceCover ? "Access to qualified engineers for covered appliance breakdowns" : null,
    hasBoilerCover ? "Access to qualified engineers for covered boiler and central heating breakdowns" : null,
    "Repairs to covered appliances or systems, where repair is possible",
    "If a repair is not economically viable, we may, at our discretion, offer a replacement of equivalent specification (new for old where applicable), subject to availability and the plan terms",
    "Fixed pricing with no call-out charge for covered faults",
    "Appointments offered subject to engineer availability"
  ].filter(Boolean);

  const coverList = coverLines.map(li => `<li><span class="tick">✓</span><span class="li">${escapeHtml(li)}</span></li>`).join("");

  return `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>The Flash Team's Protection Plan</title>
<style>
  :root{
    --navy:#0b2a4a;
    --navy2:#081f36;
    --navy3:#06162a;
    --orange:#ff6b35;
    --orange2:#ff8c42;
    --paper:#ffffff;
    --ink:#1f2a3a;
    --muted:#6b7787;
    --line:#e4e9f1;
    --bg:#f4f6fa;
  }

  *{ box-sizing:border-box; }
  html,body{ margin:0; padding:0; background:var(--bg); color:var(--ink); font-family: "Segoe UI", Arial, Helvetica, sans-serif; }

  .page{
    width: 800px;
    margin: 24px auto;
    background: var(--paper);
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 10px 24px rgba(10,20,35,.12);
    border: 1px solid rgba(11,42,74,.10);
  }

  .banner{
    position: relative;
    padding: 20px 22px 14px 22px;
    color: #fff;
    background:
      radial-gradient(1200px 240px at 20% 40%, rgba(255,255,255,.10), transparent 55%),
      radial-gradient(900px 260px at 70% 30%, rgba(255,255,255,.08), transparent 55%),
      linear-gradient(135deg, var(--navy) 0%, var(--navy2) 55%, var(--navy3) 100%);
  }
  .banner:after{
    content:"";
    position:absolute;
    left:0; right:0; bottom:0;
    height: 6px;
    background: linear-gradient(90deg, var(--orange) 0%, var(--orange2) 100%);
  }
  .brand{
    display:flex;
    align-items:center;
    justify-content:center;
    gap: 12px;
    text-align:center;
  }
  .bolt{
    width: 38px; height: 38px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange2) 100%);
    display:flex; align-items:center; justify-content:center;
    font-weight: 900;
    box-shadow: 0 6px 14px rgba(255,107,53,.35);
    color: #10243c;
    font-size: 20px;
  }
  .brandname{
    font-size: 40px;
    font-weight: 900;
    letter-spacing: .2px;
    line-height: 1;
    margin: 0;
  }
  .tagline{
    margin: 6px 0 0 0;
    font-size: 14px;
    opacity: .92;
    font-weight: 600;
  }

  .content{ padding: 22px 22px 8px 22px; }
  h1{
    margin: 12px 0 6px 0;
    font-size: 34px;
    color: var(--navy);
    letter-spacing: .2px;
  }
  .rule{
    height: 1px; background: var(--line); margin: 10px 0 16px 0;
  }
  .para{ margin: 0 0 12px 0; font-size: 14px; }
  .dear{ margin-top: 4px; }

  .active{
    border-radius: 10px;
    overflow:hidden;
    border: 1px solid rgba(10,20,35,.12);
    box-shadow: 0 6px 14px rgba(10,20,35,.08);
    margin: 14px 0 18px 0;
  }
  .active .top{
    background: linear-gradient(135deg, var(--orange) 0%, var(--orange2) 100%);
    color:#fff;
    padding: 12px 14px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap: 10px;
    font-weight: 900;
    font-size: 18px;
    text-align:center;
  }
  .active .top .miniBolt{
    width: 22px; height: 22px;
    display:inline-flex; align-items:center; justify-content:center;
    border-radius: 7px;
    background: rgba(0,0,0,.15);
    font-size: 14px;
  }
  .active .bottom{
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
    color:#eaf1ff;
    padding: 10px 14px;
    text-align:center;
    font-weight: 700;
    font-size: 13px;
  }

  .grid{
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    align-items:start;
  }
  .card{
    border: 1px solid var(--line);
    border-radius: 10px;
    overflow:hidden;
    background:#fff;
  }
  .card .head{
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
    color:#fff;
    padding: 10px 12px;
    font-weight: 900;
    font-size: 16px;
  }
  .card .body{ padding: 10px 12px 12px 12px; }

  .row{
    display:flex;
    justify-content:space-between;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid var(--line);
    font-size: 13px;
  }
  .row:last-child{ border-bottom: none; }
  .row .k{
    font-weight: 800;
    color: #1f2a3a;
  }
  .row .v{
    font-weight: 700;
    color: #2c3a52;
    text-align:right;
  }

  .kvs{ margin-bottom: 8px; }
  .kv{ font-size: 13px; margin: 0 0 6px 0; }
  .kv .k{ font-weight: 900; color: #1f2a3a; }
  .kv .v{ font-weight: 900; color: #1f2a3a; }
  .checks{ list-style:none; padding:0; margin: 8px 0 0 0; }
  .checks li{
    display:flex; gap: 8px;
    margin: 8px 0;
    font-size: 13px;
    line-height: 1.35;
  }
  .tick{
    width: 18px; height: 18px;
    border-radius: 6px;
    background: rgba(255,107,53,.18);
    display:inline-flex; align-items:center; justify-content:center;
    color: var(--orange);
    font-weight: 1000;
    flex: 0 0 18px;
  }
  .li{ color:#2a3446; font-weight: 650; }

  .below{
    margin-top: 14px;
    display:grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    align-items:start;
  }
  .steps{
    margin: 0;
    padding-left: 18px;
    font-size: 13px;
  }
  .steps li{ margin: 8px 0; }
  .phone{
    font-weight: 1000;
    color: var(--navy);
    text-decoration:none;
  }

  .dd{ margin-top: 16px; }
  .dd .body p{
    margin: 0 0 10px 0;
    font-size: 13px;
  }
  .dd ul{
    margin: 0;
    padding-left: 18px;
    font-size: 13px;
  }
  .dd li{ margin: 7px 0; }

  .important{
    margin-top: 16px;
    padding-top: 2px;
  }
  .important h2{
    margin: 0 0 8px 0;
    font-size: 18px;
    color: var(--navy);
  }
  .important ul{
    margin: 0;
    padding-left: 18px;
    font-size: 13px;
  }
  .important li{ margin: 7px 0; }

  .footer{
    margin-top: 18px;
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy2) 100%);
    color:#eaf1ff;
    padding: 12px 18px;
    font-weight: 800;
    letter-spacing: .2px;
    border-top: 6px solid;
    border-image: linear-gradient(90deg, var(--orange), var(--orange2)) 1;
    text-align:center;
    font-size: 13px;
  }
  .dots{ color: rgba(255,255,255,.6); padding: 0 6px; }

  @page { size: A4; margin: 12mm; }
  @media print{
    html,body{ background:#fff; }
    .page{
      width: auto;
      margin: 0;
      border-radius: 0;
      box-shadow: none;
      border: none;
    }
  }
</style>
</head>

<body>
  <div class="page">
    <div class="banner">
      <div class="brand">
        <div class="bolt">⚡</div>
        <div>
          <div class="brandname">Flash Team</div>
          <div class="tagline">Fast, Friendly Repairs You Can Trust</div>
        </div>
      </div>
    </div>

    <div class="content">
      <h1>The Flash Team's Protection Plan</h1>
      <div class="rule"></div>

      <p class="para dear">Dear <strong>${customerName || "{{customerName}}"}</strong>,</p>
      <p class="para">
        Thank you for choosing Flash Team. This document confirms that your <strong>Protection Plan</strong> is now active,
        subject to the plan terms, conditions and exclusions.
      </p>

      <div class="active">
        <div class="top"><span class="miniBolt">⚡</span> Your Protection Plan is now active</div>
        <div class="bottom">This letter explains your cover and how to request assistance</div>
      </div>

      <div class="grid">
        <div class="card">
          <div class="head">Your Account Details</div>
          <div class="body">
            <div class="row"><div class="k">Customer</div><div class="v">${customerName || "{{customerName}}"}</div></div>
            <div class="row"><div class="k">Email</div><div class="v">${email || "{{email}}"}</div></div>
            <div class="row"><div class="k">Phone</div><div class="v">${phone || "{{phone}}"}</div></div>
            <div class="row"><div class="k">Address</div><div class="v">${address || "{{address}}"}</div></div>
            <div class="row"><div class="k">Start Date</div><div class="v">${coverageStartDate || "{{coverageStartDate}}"}</div></div>
            <div class="row"><div class="k">Policy Ref</div><div class="v">${policyNumber || "{{policyNumber}}"}</div></div>
          </div>
        </div>

        <div class="card">
          <div class="head">What Your Plan Provides</div>
          <div class="body">
            <div class="kvs">
              ${monthlyLine}
            </div>
            <ul class="checks">
              ${coverList}
            </ul>
          </div>
        </div>
      </div>

      <div class="below">
        <div class="card">
          <div class="head">Requesting Assistance</div>
          <div class="body">
            <ol class="steps">
              <li>Call <a class="phone" href="tel:03308227695">0330 822 7695</a></li>
              <li>Quote your policy reference <strong>${policyNumber || "{{policyNumber}}"}</strong></li>
              <li>Describe the issue so we can assess eligibility</li>
              <li>Book an appointment subject to availability</li>
            </ol>
          </div>
        </div>

        <div></div>
      </div>

      <div class="card dd">
        <div class="head">Direct Debit Guarantee</div>
        <div class="body">
          <p>If you pay by <strong>Direct Debit</strong>, payments will appear on your bank statement as <strong>Warmcare</strong>.</p>
          <ul>
            <li>The Direct Debit Guarantee is offered by all banks and building societies that accept instructions to pay Direct Debits.</li>
            <li>If there are any changes to the amount, date or frequency of your Direct Debit, you will be notified in advance.</li>
            <li>If an error is made in the payment of your Direct Debit, you are entitled to a full and immediate refund from your bank or building society.</li>
            <li>You can cancel a Direct Debit at any time by contacting your bank or building society. Written confirmation may be required.</li>
          </ul>
        </div>
      </div>

      <div class="important">
        <h2>Important Information</h2>
        <ul>
          <li>This Protection Plan is a <strong>service agreement</strong> and is not an insurance policy.</li>
          <li>All services are provided subject to <strong>plan terms, conditions and exclusions</strong>.</li>
          <li>Annual boiler service: Please contact us to book your annual boiler service.</li>
        </ul>
      </div>

      <div class="footer">
        Flash Team <span class="dots">•</span> Nationwide UK <span class="dots">•</span> 0330 822 7695 <span class="dots">•</span> theflashteam.co.uk
      </div>
    </div>
  </div>
</body>
</html>`;
}

async function generateProtectionPlanPdf(data: any): Promise<{ filename: string; contentType: string; bytes: Buffer }> {
  const html = buildHtml(data);

  const browser = await chromium.launch({
    headless: true,
    args: ["--font-render-hinting=medium"]
  });

  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "networkidle" });
    await page.emulateMedia({ media: "print" });

    const pdfBytes = await page.pdf({
      format: "A4",
      printBackground: true,
      margin: { top: "12mm", right: "12mm", bottom: "12mm", left: "12mm" },
      preferCSSPageSize: true
    });

    const ref = safeFilename((data && data.policyNumber) ? `protection-plan-${data.policyNumber}` : "protection-plan");
    return {
      filename: `${ref}.pdf`,
      contentType: "application/pdf",
      bytes: Buffer.from(pdfBytes)
    };
  } finally {
    await browser.close();
  }
}

export async function POST(req: NextRequest) {
  try {
    const session = await getServerSession(authOptions);
    
    if (!session || session.user.role !== 'ADMIN') {
      return NextResponse.json(
        { error: 'Unauthorized' }, 
        { status: 401 }
      );
    }

    const { saleId, templateType, templateId } = await req.json();

    if (!saleId || !templateType) {
      return NextResponse.json(
        { error: 'Missing required fields: saleId and templateType' },
        { status: 400 }
      );
    }

    console.log(`🎯 Direct PDF generation request:`, { saleId, templateType, templateId });

    // Get sale data
    const sale = await prisma.sale.findUnique({
      where: { id: saleId },
      include: {
        appliances: true,
        createdBy: true,
      },
    });

    if (!sale) {
      return NextResponse.json(
        { error: 'Sale not found' },
        { status: 404 }
      );
    }

    console.log(`📄 Generating PDF for customer: ${sale.customerFirstName} ${sale.customerLastName}`);

    // Prepare data for the PDF generator
    const pdfData = {
      customerName: `${sale.customerFirstName} ${sale.customerLastName}`.trim(),
      email: sale.email,
      phone: sale.phoneNumber,
      address: [sale.mailingStreet, sale.mailingCity, sale.mailingProvince, sale.mailingPostalCode]
        .filter(Boolean)
        .join('\n'),
      coverageStartDate: sale.directDebitDate,
      policyNumber: sale.id.toUpperCase(),
      monthlyCost: sale.totalPlanCost,
      hasApplianceCover: sale.applianceCoverSelected,
      hasBoilerCover: sale.boilerCoverSelected,
    };

    // Generate the perfect PDF using the Flash Team generator
    const { filename, contentType, bytes } = await generateProtectionPlanPdf(pdfData);

    console.log(`✅ Perfect PDF generated: ${filename} (${bytes.length} bytes)`);

    // Convert buffer to Uint8Array for Response
    const uint8Buffer = new Uint8Array(bytes);

    // Return PDF as response
    return new Response(uint8Buffer, {
      status: 200,
      headers: {
        'Content-Type': contentType,
        'Content-Disposition': `attachment; filename="${filename}"`,
        'Content-Length': bytes.length.toString(),
      },
    });

  } catch (error) {
    console.error('❌ Perfect PDF generation failed:', error);
    
    return NextResponse.json(
      { 
        error: 'PDF generation failed',
        details: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
}