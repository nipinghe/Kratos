domain_size = *GenData(DOMAIN_SIZE)

#Problem Data
#####################################

ProblemType = "*GenData(Problem_Type)"
NumberofThreads = *GenData(Number_of_threads,INT)
Solution_method = "Newton-Raphson"		
SolverType  = "*GenData(Solver_Type)"
time_step = *GenData(Time_Step)
nsteps = *GenData(Number_of_steps,INT)

#Solver Data
#####################################

class SolverSettings:
    solver_type  = "mechanical_solver"
    domain_size  = *GenData(DOMAIN_SIZE,INT)
    RotationDofs = False
    PressureDofs = False
    RigidWalls = *GenData(Rigid_Wall_Contact)
    ReformDofSetAtEachStep = True
    compute_reactions = True
    line_search = *GenData(LineSearch)
    scheme_type = "*GenData(Solver_Type)"
    convergence_criterion = "*GenData(Convergence_Criteria)"
*format "%10.5e"
    displacement_relative_tolerance = *GenData(Convergence_Tolerance)
*format "%10.5e"
    displacement_absolute_tolerance = *GenData(Absolute_Tolerance)
*format "%10.5e"		      
    residual_relative_tolerance = *GenData(Convergence_Tolerance)
*format "%10.5e"
    residual_absolute_tolerance = *GenData(Absolute_Tolerance)
*format "%4i"
    max_iteration = *GenData(Max_Iter,INT)

    class linear_solver_config:
	solver_type   = "*GenData(Linear_Solver)"
	scaling       = False
	tolerance     = 1e-7
	max_iteration = *GenData(Linear_Solver_Max_Iteration,INT) #300 
	verbosity     = 0
	is_symmetric  = False  
	
	#Pastix Iterative Solver:
        gmres_krylov_space_dimension = 100
        ilu_level_of_fill            = 3 #5

        #GMRES or CG:
        preconditioner_type          = "None"

        #Deflated CG:
        assume_constant_structure    = True
        max_reduced_size             = 1000

        #AMG: (requires ResidualBasedBlockBuilderAndSolver )
        smoother_type  = "ILU0" #"DAMPED_JACOBI"
        krylov_type    = "GMRES"
	

#Meshing Data
#####################################

RemeshDomains  = *GenData(RemeshDomains)
MeshingElement = "*GenData(MeshingElement)"
RefineDomains  = False
MeshConditions = []
*for(i=1;i<=GenData(MeshDomains,INT);i=i+7)
*set var ndomains(int)=Operation(ndomains(int)+1)
Conditions*ndomains = {"Subdomain":*GenData(MeshDomains,*i), "Remesh":*GenData(MeshDomains,*Operation(i+1)), "Constrained":*GenData(MeshDomains,*Operation(i+2)), "Refine":*GenData(MeshDomains,*Operation(i+3)), "MeshSmoothing":*GenData(MeshDomains,*Operation(i+4)), "JacobiSmoothing":*GenData(MeshDomains,*Operation(i+5)), "MeshElement":"*GenData(MeshDomains,*Operation(i+6))"}
MeshConditions.append(Conditions*ndomains)
*end

BoxCenter = []
BoxCenter.append(*GenData(Center_box,1))
BoxCenter.append(*GenData(Center_box,2))
BoxCenter.append(0)

BoxVelocity = [] 
BoxVelocity.append(*GenData(Velocity_box,1))
BoxVelocity.append(*GenData(Velocity_box,2))
BoxVelocity.append(0)

#set mesh modeler configuration
class mesh_modeler_config:
    number_domains = *ndomains
    size_scale = 1
    critical_radius = *GenData(Critical_Mesh_Size)
    critical_dissipation = *GenData(Critical_Dissipation)
    reference_error = *GenData(Critical_Error)
    offset_factor = *GenData(Offset_Factor)   			  
    mesh_conditions = MeshConditions
    box_refinement_only = "*GenData(Refine_on_box_only)"
    box_center = BoxCenter
    box_velocity = BoxVelocity
    box_radius = *GenData(Radius_box)
    remesh_frequency = *GenData(Meshing_Frequency)

#Contact Data
#####################################

FindContacts = *GenData(FindContacts)

class contact_modeler_config:
    contact_condition        = "*GenData(ContactCondition)"
    constrained_contact      = *GenData(Constrained_Contact)
    friction_active          = *GenData(Friction_Active)
    mu_static                = 0.3
    mu_dynamic               = 0.2
    offset_factor            = *GenData(Offset_Factor)
    penalty_parameter        = *GenData(Penalty_Parameter)
    stability_parameter      = *GenData(Stability_Parameter)
    contact_search_frequency = *GenData(Contact_Search_Frequency)

#set rigid wall configuration
class rigid_wall_config:
    rigid_wall         = *GenData(Rigid_Wall_Contact)
    size_scale         = 1
    tip_radius         = *GenData(Tip_Radius)
    rake_angle         = *GenData(Rake_Angle)
    clearance_angle    = *GenData(Clearance_Angle)
    penalty_parameter  = *GenData(Rigid_Body_Penalty_Parameter)
    center = []
    center.append(*GenData(Reference_Point_definition,1))
    center.append(*GenData(Reference_Point_definition,2))
    center.append(0)
    velocity = [] 
    velocity.append(*GenData(Velocity_definition,1))
    velocity.append(*GenData(Velocity_definition,2))
    velocity.append(0)


#Constraints Data
#####################################

Incremental_Load = "*GenData(Incremental_Load)"
Incremental_Displacement = "*GenData(Incremental_Displacement)"

#PostProcess Data
#####################################

nodal_results=["DISPLACEMENT","REACTION","NORMAL","CONTACT_FORCE"]
gauss_points_results=["GREEN_LAGRANGE_STRAIN_TENSOR","CAUCHY_STRESS_TENSOR","FORCE"]

# GiD output configuration
class GidOutputConfiguration:
    GiDPostMode = "*GenData(FileFormat)"
*if(strcmp(GenData(WriteMesh),"Deformed")==0)
    GiDWriteMeshFlag = True
*else
    GiDWriteMeshFlag = False
*endif
    GiDWriteConditionsFlag = *GenData(WriteConditions)
    GiDWriteParticlesFlag = *GenData(WriteParticles)
    GiDMultiFileFlag = "Multiples"

GiDWriteFrequency = *GenData(WriteFrequency)
WriteResults = "*GenData(WriteResults)"
echo_level = *GenData(Echo_Level)

# graph_options
PlotGraphs = "*GenData(Plot_Graphs)"
PlotFrequency = *GenData(PlotFrequency)

# list options
PrintLists = "*GenData(Print_List_Files)"
number_of_lists = *GenData(List_Files)
file_list = []
*for(i=1;i<=GenData(List_Files,INT);i=i+1)
file_list.append(*GenData(List_Files,*i))
*end

# restart options
SaveRestart = "*GenData(Print_Restart)"
RestartFrequency = *GenData(Restart_Interval)
LoadRestart = "*GenData(Load_Restart)"
Restart_Step = *GenData(Load_Step)

# Declare Python Variables

