package aitl

#OutcomeRequest: {
	kind: _
	if kind == "development" {
		// ADR-016@v3 C15: this ADR isn't applied to hand-built development outcomes
		applies: "ADR-016": false
	}
}
