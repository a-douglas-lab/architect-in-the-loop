package payments

import (
	"aitl.example/domains/canon"
	"aitl.example/domains/policy/auth"
	"aitl.example/domains/policy/data"
	"aitl.example/domains/capability/workflow"
)

endpoints: [...auth.#Endpoint] & [
	{path: "/payments", method: "POST", auth: "required", roles: ["customer"], admin: false, mfa: false},
	{path: "/payments/admin/refund", method: "POST", auth: "required", roles: ["finance"], admin: true, mfa: false},
]

charge: canon.#Money & {amount: 1999, currency: "GBP"}
fxCharge: canon.#Money & {amount: 500, currency: "USD"}

events: captured: data.#Event & {
	name:          "PaymentCaptured"
	schemaVersion: 1
	retentionDays: 2555
	financial:     true
	hasPII:        true
	payload: {
		customer: canon.#CustomerRef & {customerId: "c-1", email: {value: "a@example.com", classification: "personal"}}
		amount: charge
	}
}

workflows: refund: workflow.#Workflow & {
	name: "refund"
	steps: [{name: "issue-refund", sideEffect: true, timeoutHours: 2, compensation: "reverse-refund"}]
}
