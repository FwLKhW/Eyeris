_:
    @just --list

# Format
fmt:
    @cargo fmt

# Lint
lint:
    @cargo clippy --all-targets --all-features -- -D warnings

# Test
test:
    @cargo nextest run --workspace --bins --all-targets --cargo-quiet --cargo-quiet --no-tests pass

# Format + Lint + Test
ci: fmt lint test

# Run Dev
r *args:
    @cargo r {{args}}

# Run Release
rr *args:
    @cargo r --release {{args}}
