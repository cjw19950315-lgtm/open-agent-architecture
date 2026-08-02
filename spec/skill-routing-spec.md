# Dynamic Skill Routing & Precondition Memory Specification

Version: 1.0.0

## Intent Compression Algorithm

When a request arrives, the routing engine compresses the request into 5 key dimension fields:
1. `final_artifact`
2. `input_source`
3. `primary_action`
4. `business_domain`
5. `risk_level`

## Selection Rules

- **Maximum Allocation**: Max 1 primary skill + 2 auxiliary skills per turn.
- **Precondition Memory**: Before selecting a tool, check `tool-preconditions` for known failure fingerprints.
- **Fast-Path Priority**: Prefer local verified paths over unverified remote network calls.
