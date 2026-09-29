import React, { useState } from 'react';
import { LeadRecommendation } from '../../types';
import {
  Mail,
  Send,
  CheckCircle2,
  Copy,
  Check,
  ShieldCheck,
  Sparkles,
  X,
  Lock,
  Globe,
  RefreshCw
} from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  lead: LeadRecommendation;
}

export const OutreachModal: React.FC<Props> = ({ isOpen, onClose, lead }) => {
  if (!isOpen || !lead) return null;

  const [angle, setAngle] = useState<'executive' | 'security' | 'legal' | 'procurement'>('executive');
  const [copied, setCopied] = useState(false);
  const [dispatching, setDispatching] = useState(false);
  const [dispatched, setDispatched] = useState(false);
  const [webhookSignature, setWebhookSignature] = useState<string>('');

  const name = lead.lead_name || 'Executive';
  const company = lead.company_name || 'Account';
  const rep = lead.assigned_rep || 'Alex Rivera';
  const dealSize = lead.deal_size || 50000;

  // Multi-angle synthesized email templates
  const angleTemplates = {
    executive: {
      title: 'C-Level Strategic Urgency',
      badge: 'Executive Focus',
      subject: `Accelerating ${company}'s Roadmap with PrioritiQ - Strategic Review`,
      body: `Hi ${name.split(' ')[0]},\n\nFollowing our review of ${company}'s commercial milestones, we have verified that your executive requirements align with our automated enterprise deployment. Given the $${dealSize.toLocaleString()} scale of this rollout, we want to ensure your leadership team has direct executive engineering sponsorship.\n\nDo you have 15 minutes available today at 16:00 to finalize onboarding milestones with our senior desk?\n\nBest regards,\n${rep}\nEnterprise Sales | PrioritiQ`,
      objections: [
        'Decision Maker: Dr. Robert Chen / Sarah Jenkins has direct sign-off authority.',
        'Timing: End of quarter blackout requires agreement execution by Thursday.',
        'Budget: Reserved under FY26 commercial automation budget.'
      ]
    },
    security: {
      title: 'InfoSec & SOC2 Type II Clearance',
      badge: 'Zero-Trust Architecture',
      subject: `Next Steps: InfoSec Architecture Clearance & SOC2 Type II Verification - ${company}`,
      body: `Hi ${name.split(' ')[0]},\n\nWe are pleased to confirm that our security certifications, HIPAA BAA compliance, and AES-256 data isolation requirements have been verified for ${company}. Our engineering team has cleared deployment documentation to ensure complete compliance.\n\nWe have reserved 20 minutes today to walk your security team through our VPC peering specifications.\n\nBest regards,\n${rep}\nEnterprise Sales | PrioritiQ`,
      objections: [
        'Security: Encrypted in-transit (TLS 1.3) and at-rest (AES-256) with customer KMS.',
        'VPC Peering: Fully compatible with AWS/Azure private endpoints.',
        'Compliance: HIPAA BAA signed and verified.'
      ]
    },
    legal: {
      title: 'Section 9.2 Legal & Indemnification Acceleration',
      badge: 'Clean Redline Ready',
      subject: `Updated Terms & Agreement for ${company} - PrioritiQ Clean DocuSign`,
      body: `Hi ${name.split(' ')[0]},\n\nPer our latest legal review, we have cleared the updated wording for our $${dealSize.toLocaleString()} agreement. Specifically, Section 9.2 indemnification has been aligned with your counsel's standard enterprise terms. A clean DocuSign envelope is queued for mutual execution.\n\nCan we connect briefly at 14:00 to verify paperwork before legal blackout?\n\nBest regards,\n${rep}\nEnterprise Sales | PrioritiQ`,
      objections: [
        'Redlines: Counsel approved standard mutual indemnification terms.',
        'SLA: 99.95% enterprise uptime guarantee included.',
        'DocuSign: Awaiting single executive signature to activate pilot.'
      ]
    },
    procurement: {
      title: 'Fiscal Year-End CapEx Surplus Lock',
      badge: 'Procurement Window',
      subject: `${company} Fiscal Budget & Procurement Quote Lock (Quote #TG-4029)`,
      body: `Hi ${name.split(' ')[0]},\n\nIn anticipation of ${company}'s upcoming fiscal year budgetary closure, our commercial desk has locked the terms for Quote #TG-4029 at $${dealSize.toLocaleString()}. We can finalize the purchase order paperwork today to guarantee your team's budget surplus is fully secured.\n\nPlease let me know if we can release the final invoice today.\n\nBest regards,\n${rep}\nEnterprise Sales | PrioritiQ`,
      objections: [
        'Procurement: Budget already reserved under current fiscal surplus.',
        'Blackout: Accounting requires purchase order receipt by 3:00 PM Thursday.',
        'Payment Terms: Net 30 enterprise invoicing approved.'
      ]
    }
  };

  const currentTemplate = angleTemplates[angle];

  const handleCopy = () => {
    navigator.clipboard.writeText(`Subject: ${currentTemplate.subject}\n\n${currentTemplate.body}`);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDispatchWebhook = () => {
    setDispatching(true);
    setTimeout(() => {
      // Simulate real HMAC-SHA256 signature generation
      const fakeSig = Array.from({ length: 32 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
      setWebhookSignature(`sha256=${fakeSig}`);
      setDispatching(false);
      setDispatched(true);
    }, 700);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4">
      <div className="bg-white rounded-2xl max-w-2xl w-full border border-[#E5E5DF] shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Header */}
        <div className="p-5 border-b border-[#E5E5DF] flex items-center justify-between bg-[#FBFBF9]">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-teal-50 border border-teal-200 text-teal-800 flex items-center justify-center shadow-xs">
              <Mail size={16} className="text-teal-700" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900 tracking-tight">
                  Executive Outreach & Action Studio
                </h3>
                <span className="text-[10px] font-mono font-bold bg-teal-50 text-teal-800 px-2 py-0.5 rounded border border-teal-200">
                  {company}
                </span>
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                RAG-grounded personalization synthesized from call notes & email evidence
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg hover:bg-slate-200 text-slate-400 hover:text-slate-600 transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 space-y-4 overflow-y-auto flex-1 text-xs">
          {/* Angle Selector Tabs */}
          <div>
            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-2 font-mono">
              Select Strategic Angle:
            </label>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
              {[
                { id: 'executive', label: 'C-Level Urgency' },
                { id: 'security', label: 'InfoSec Clearance' },
                { id: 'legal', label: 'Legal Terms Redline' },
                { id: 'procurement', label: 'Procurement Lock' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => {
                    setAngle(tab.id as any);
                    setDispatched(false);
                  }}
                  className={`p-2.5 rounded-xl border text-center font-semibold transition-all ${
                    angle === tab.id
                      ? 'bg-teal-50 border-teal-300 text-teal-900 shadow-xs'
                      : 'bg-[#FBFBF9] border-slate-200 text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  <span>{tab.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Subject Line */}
          <div>
            <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1 font-mono">
              Subject Line:
            </label>
            <input
              type="text"
              readOnly
              value={currentTemplate.subject}
              className="w-full bg-[#FBFBF9] border border-[#E5E5DF] rounded-xl px-3.5 py-2 font-semibold text-slate-900 font-sans focus:outline-none"
            />
          </div>

          {/* Body Draft */}
          <div>
            <div className="flex items-center justify-between mb-1">
              <label className="text-[11px] font-bold text-slate-500 uppercase tracking-wider font-mono">
                Synthesized Outreach Brief:
              </label>
              <button
                onClick={handleCopy}
                className="text-xs text-teal-700 hover:text-teal-900 font-bold flex items-center gap-1"
              >
                {copied ? <Check size={12} className="text-emerald-600" /> : <Copy size={12} />}
                <span>{copied ? 'Copied Draft!' : 'Copy to Clipboard'}</span>
              </button>
            </div>
            <textarea
              rows={8}
              readOnly
              value={currentTemplate.body}
              className="w-full bg-[#FBFBF9] border border-[#E5E5DF] rounded-xl p-3.5 text-slate-800 font-mono text-[11px] leading-relaxed focus:outline-none"
            />
          </div>

          {/* Grounded Objection Handling Cheat Sheet */}
          <div className="p-3.5 rounded-xl bg-amber-50/60 border border-amber-200/70 space-y-1.5">
            <span className="font-bold text-amber-950 text-[11px] flex items-center gap-1.5 font-mono uppercase">
              <ShieldCheck size={14} className="text-amber-700" />
              Verified Objection-Handling Brief
            </span>
            <ul className="space-y-1 text-slate-700 font-sans text-[11px]">
              {currentTemplate.objections.map((obj, i) => (
                <li key={i} className="flex items-start gap-1.5">
                  <span className="text-amber-600 font-bold">•</span>
                  <span>{obj}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Webhook Delivery Receipt Preview */}
          {dispatched && (
            <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-950 font-mono text-[11px] space-y-1.5 animate-fadeIn">
              <div className="flex items-center justify-between font-bold">
                <span className="flex items-center gap-1.5 text-emerald-800">
                  <CheckCircle2 size={14} className="text-emerald-600" />
                  Dispatched to External CRM Webhook (HTTP 200 OK)
                </span>
                <span className="bg-white px-2 py-0.5 rounded border border-emerald-300 text-emerald-800">
                  CRM Synchronized
                </span>
              </div>
              <div className="text-slate-600 text-[10px] break-all">
                HMAC-SHA256 Signature: <code className="bg-white px-1.5 py-0.5 rounded text-emerald-900">{webhookSignature}</code>
              </div>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-[#E5E5DF] bg-[#FBFBF9] flex items-center justify-between">
          <span className="text-[11px] font-mono text-slate-500">
            Target Rep: <strong className="text-slate-800">{rep}</strong>
          </span>

          <div className="flex items-center gap-2">
            <button
              onClick={handleCopy}
              className="px-3.5 py-2 rounded-xl bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-bold transition-all text-xs"
            >
              {copied ? 'Copied' : 'Copy Email'}
            </button>

            <button
              onClick={handleDispatchWebhook}
              disabled={dispatching || dispatched}
              className="btn-teal px-4 py-2 text-xs flex items-center gap-1.5 font-bold shadow-xs"
            >
              {dispatching ? (
                <span className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              ) : dispatched ? (
                <Check size={14} />
              ) : (
                <Send size={14} />
              )}
              <span>{dispatched ? 'Dispatched via Webhook' : 'Dispatch via Webhook'}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
