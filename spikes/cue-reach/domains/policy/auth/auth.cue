package auth

// A cross-cutting ADR on authentication and authorisation, applied to every domain's endpoints.

publicPaths: ["/health", "/catalog"]

#Endpoint: {
	path:   string
	method: "GET" | "POST" | "PUT" | "DELETE"
	auth:   "required" | "none"
	roles: [...string]
	admin: bool
	mfa:   bool
	if auth == "none" {
		// Auth ADR C1: only public paths may skip authentication
		path: or(publicPaths)
	}
	if method != "GET" {
		// Auth ADR C2: a write endpoint names at least one role
		roles: [_, ...]
	}
}
