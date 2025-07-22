using Gridap
using GridapGmsh
using Plots

models = [GmshDiscreteModel("mesh_A.msh"),
          GmshDiscreteModel("mesh_B.msh"),
          GmshDiscreteModel("mesh_C.msh")]

r = 20.0
Δp = 3.0 * 9.80665
L = 300.0 * 1e3  # 300 μm = 300000 nm
μ = 0.0015
f(x) = Δp/L/μ
g = 0.0
order = 1
reffe = ReferenceFE(lagrangian, Float64, order)
peclet_values = Float64[]

for (idx, model) in enumerate(models)
    if idx == 1  
        boundary_tags = ["Boundary_1", "Boundary_2", "Boundary_3"]
        n_boundaries = 3
    elseif idx == 2  
        boundary_tags = ["Boundary_1", "Boundary_2", "Boundary_3", "Boundary_4"]
        n_boundaries = 4
    else  
        boundary_tags = ["Boundary_1", "Boundary_2", "Boundary_3", "Boundary_4", "Boundary_5"]
        n_boundaries = 5
    end

    V = TestFESpace(model, reffe, dirichlet_tags=boundary_tags)
    U = TrialFESpace(V, fill(g, n_boundaries))

    Ω = Triangulation(model)
    dΩ = Measure(Ω, 2*order)

    a(u,v) = ∫( ∇(v)⋅∇(u) )dΩ
    l(v) = ∫(f*v)dΩ
    op = AffineFEOperator(a, l, U, V)
    uh = solve(op)

    S = sum( ∫(1)*dΩ )
    Q = sum( ∫(uh)*dΩ )
    velocity = Q/S
    D = 62e3  
    Peclet = L*velocity/D
    push!(peclet_values, Peclet)

    println("\nResults for configuration $idx:")
    println("Тип: ", idx == 1 ? "A (Triangular)" : idx == 2 ? "B (Square)" : "C (4 large + 1 small)")
    println("Flow = ", Q, " nm³/s")
    println("Area = ", S, " nm²")
    println("Average speed = ", velocity, " nm/s")
    println("Pekle's Number = ", Peclet)

    writevtk(Ω, "solution_$idx", cellfields=["uh" => uh])
end

labels = ["A (Triangular)", "B (Square)", "C (4 large + 1 small)"]
plot(1:3, peclet_values, 
    label="Pekle's Number", 
    xlabel="Packaging type", 
    ylabel="Meaning", 
    title="Comparison of Peclet number",
    xticks=(1:3, labels),
    markershape=:circle,
    linewidth=2,
    legend=:topright,
    framestyle=:box
)

savefig("peclet_comparison.png")
println("\nGraph saved as peclet_comparison.png")