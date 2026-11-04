package aitl

#PlanCitations: {
	// ADR-009@v3 C8: every plan lists the ADRs that apply
	adrs: [_, ...]
	// ADR-009@v3 C13 and ADR-000@v4 C10: every citation records the ADR's version, as ADR-nnn@vN Cn
	citations: [...=~"^ADR-[0-9]{3}@v[0-9]+ C[0-9]+$"]
}
