stretch(α=1, β=1) = [α 0; 0 β]

rotate(θ) = [cos(θ) -sin(θ); sin(θ) cos(θ)]

transform(x, y, θ=0, α=1, β=1) = hcat(x, y) * rotate(θ) * stretch(α, β)

compare_angles(ϕ, ψ) = ((Δ = ϕ - ψ) > π ? Δ - 2π : (Δ < -π ? Δ + 2π : Δ))

translate(x, y, x0, y0) = hcat(x .- x0, y .- y0)

convolve(x, y, u, v) = @. exp(-2im * π * (x * u + y * v))
