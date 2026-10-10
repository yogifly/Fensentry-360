import { describe, expect, it } from 'vitest';
import type { RiskResult } from './types';

describe('FinSentry frontend contract', () => {
  it('models the backend risk response shape', () => {
    const result: RiskResult = {
      risk_score: 91, risk_probability: 0.91, risk_level: 'CRITICAL',
      recommended_action: 'BLOCK', reasons: ['Active phone call detected'],
      transaction_id: 1, cooldown_required: true, cooldown_seconds: 10,
    };
    expect(result.risk_score).toBeGreaterThan(80);
    expect(result.cooldown_required).toBe(true);
  });
});
