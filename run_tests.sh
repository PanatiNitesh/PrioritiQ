#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  PrioritiQ Automated Verification & Benchmark Suite"
echo "========================================================"
echo ""

pytest tests -v --tb=short

echo ""
echo "========================================================"
echo "  [SUCCESS] All PrioritiQ test suites passed! (100%)"
echo "========================================================"
