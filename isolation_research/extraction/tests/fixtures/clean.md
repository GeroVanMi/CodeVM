# Fake Source

We recommend running the agent inside a virtual machine, because a shared
kernel “is not a security boundary” for untrusted code — at least not today.

The ﬁrewall must deny all egress by default; per-domain allow-
lists can be bypassed via DNS tunneling.

Attackers can hide instructions in README files and issue comments.

Never mount the Docker socket into the sandbox; it exposes the host. Treat AI-
generated git hooks as untrusted before they run on the host, since your
cloud credentials are at stake.
