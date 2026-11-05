package data

// A cross-cutting ADR for the data platform, applied to every domain's events.

maxRetentionDays: 365

#PIIField: {
	value: string
	// Data ADR C3: a PII field carries its classification
	classification: "personal" | "sensitive"
}

#Event: {
	name: string
	// Data ADR C1: every event has a schema version
	schemaVersion: int & >=1
	retentionDays: int & >0
	financial:     bool | *false
	hasPII:        bool | *false
	if !financial {
		// Data ADR C2: operational events are kept no longer than the limit
		retentionDays: <=maxRetentionDays
	}
	...
}
