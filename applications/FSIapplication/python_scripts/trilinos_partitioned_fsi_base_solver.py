from __future__ import print_function, absolute_import, division  # makes KratosMultiphysics backward compatible with python 2.6 and 2.7

# Import utilities
# import NonConformant_OneSideMap                # Import non-conformant mapper TODO: CALL THE MAPPING APPLICATION MAPPER
import python_solvers_wrapper_fluid            # Import the fluid Python solvers wrapper

# Import kratos core and applications
import KratosMultiphysics
import KratosMultiphysics.mpi as KratosMPI
import KratosMultiphysics.MetisApplication as KratosMetis
import KratosMultiphysics.TrilinosApplication as KratosTrilinos
import KratosMultiphysics.ALEApplication as KratosALE
import KratosMultiphysics.MappingApplication as KratosMapping
import KratosMultiphysics.FSIApplication as KratosFSI
import KratosMultiphysics.FluidDynamicsApplication as KratosFluid
import KratosMultiphysics.StructuralMechanicsApplication as KratosStructural

# Check that KratosMultiphysics was imported in the main script
KratosMultiphysics.CheckForPreviousImport()

## Import base class file
import partitioned_fsi_base_solver


def CreateSolver(structure_main_model_part, fluid_main_model_part, project_parameters):
    return TrilinosPartitionedFSIBaseSolver(structure_main_model_part, fluid_main_model_part, project_parameters)


class TrilinosPartitionedFSIBaseSolver(partitioned_fsi_base_solver.PartitionedFSIBaseSolver):
    def __init__(self, structure_main_model_part, fluid_main_model_part, project_parameters):

        if (KratosMPI.mpi.rank == 0) : print("** Calling the partitioned FSI Trilinos base solver constructor...")

        #TODO: Overwrite the fields in the base class default_settings and call the base class constructor?¿?¿

        # Initial tests
        start_time_structure = project_parameters["structure_solver_settings"]["problem_data"]["start_time"].GetDouble()
        start_time_fluid = project_parameters["fluid_solver_settings"]["problem_data"]["start_time"].GetDouble()
        end_time_structure = project_parameters["structure_solver_settings"]["problem_data"]["end_time"].GetDouble()
        end_time_fluid = project_parameters["fluid_solver_settings"]["problem_data"]["end_time"].GetDouble()

        if start_time_structure != start_time_fluid:
            if (KratosMPI.mpi.rank == 0) : raise("ERROR: Different initial time among subdomains!")
        if end_time_structure != end_time_fluid:
            if (KratosMPI.mpi.rank == 0) : raise("ERROR: Different final time among subdomains!")

        #TODO: shall obtain the compute_model_part from the MODEL once the object is implemented
        self.structure_main_model_part = structure_main_model_part
        self.fluid_main_model_part = fluid_main_model_part

        # Settings string in JSON format
        default_settings = KratosMultiphysics.Parameters("""
        {
        "structure_solver_settings":
            {
            "solver_type" : "trilinos_structural_mechanics_implicit_dynamic_solver",
            "model_import_settings" : {
                "input_type"     : "mdpa",
                "input_filename" : "unknown_name"
            },
            "material_import_settings" :{
                "materials_filename" : "materials.json"
            },
            "echo_level"               : 0,
            "time_integration_method"  : "Implicit",
            "analysis_type"            : "nonlinear",
            "rotation_dofs"            : false,
            "pressure_dofs"            : false,
            "reform_dofs_at_each_step" : false,
            "line_search"              : false,
            "compute_reactions"        : true,
            "compute_contact_forces"   : false,
            "block_builder"            : true,
            "move_mesh_flag"           : true,
            "solution_type"            : "Dynamic",
            "scheme_type"              : "Newmark",
            "convergence_criterion"    : "Residual_criteria",
            "displacement_relative_tolerance" : 1.0e-3,
            "displacement_absolute_tolerance" : 1.0e-5,
            "residual_relative_tolerance"     : 1.0e-3,
            "residual_absolute_tolerance"     : 1.0e-5,
            "max_iteration"          : 10,
            "linear_solver_settings" :{
                "solver_type" : "Klu",
                "scaling"     : false
            },
            "processes_sub_model_part_list"      : [""],
            "problem_domain_sub_model_part_list" : [""]
            },
        "fluid_solver_settings" : {
            "solver_type"       : "Monolithic",
            "model_import_settings" : {
                "input_type"     : "mdpa",
                "input_filename" : "unknown_name"
            },
            "maximum_iterations" : 10,
            "dynamic_tau"        : 0.01,
            "oss_switch"         : 0,
            "echo_level"         : 0,
            "consider_periodic_conditions" : false,
            "compute_reactions"            : true,
            "divergence_clearance_steps"   : 0,
            "reform_dofs_at_each_step"     : true,
            "relative_velocity_tolerance"  : 1e-3,
            "absolute_velocity_tolerance"  : 1e-5,
            "relative_pressure_tolerance"  : 1e-3,
            "absolute_pressure_tolerance"  : 1e-5,
            "linear_solver_settings"        : {
                "solver_type"                        : "MultiLevelSolver",
                "max_iteration"                      : 200,
                "tolerance"                          : 1e-8,
                "max_levels"                         : 3,
                "symmetric"                          : false,
                "reform_preconditioner_at_each_step" : true,
                "scaling"                            : true
            },
            "volume_model_part_name" : "volume_model_part",
            "skin_parts"             : [""],
            "no_skin_parts"          : [""],
            "time_stepping"          : {
                "automatic_time_step" : false,
                "time_step"           : 0.1
            },
            "alpha"              :-0.3,
            "move_mesh_strategy" : 0,
            "periodic"           : "periodic",
            "move_mesh_flag"     : false,
            "turbulence_model"   : "None"
            },
        "coupling_solver_settings": {
            "coupling_scheme"              : "DirichletNeumann",
            "solver_type"                  : "trilinos_partitioned_fsi_solver",
            "nl_tol"                       : 1e-5,
            "nl_max_it"                    : 50,
            "solve_mesh_at_each_iteration" : true,
            "coupling_strategy" : {
                "solver_type"       : "Relaxation",
                "acceleration_type" : "Aitken",
                "w_0"               : 0.825
            },
            "mesh_solver"                : "trilinos_mesh_solver_structural_similarity",
            "mesh_reform_dofs_each_step" : false,
            "structure_interfaces_list"  : [""],
            "fluid_interfaces_list"      : [""]
            },
        "mapper_settings" : [{
            "mapper_face"                                : "Unique",
            "positive_fluid_interface_submodelpart_name" : "Default_interface_submodelpart_name",
            "structure_interface_submodelpart_name"      : "Default_interface_submodelpart_name"
            }]
        }
        """)

        # Time stepping checks (no sub-stepping between subdomains has been implemented yed)
        time_step_structure = project_parameters["structure_solver_settings"]["problem_data"]["time_step"].GetDouble()
        # If automatic time stepping has been selected in the fluid domain, deactivate it and use the structure time step
        if (project_parameters["fluid_solver_settings"]["solver_settings"]["time_stepping"]["automatic_time_step"].GetBool()):
            project_parameters["fluid_solver_settings"]["solver_settings"]["time_stepping"]["automatic_time_step"].SetBool(False)
            time_step_fluid = time_step_structure
            if (KratosMPI.mpi.rank == 0) : print("WARNING: Automatic fluid time stepping cannot be used. Setting structure time step as fluid time step.")
        else:
            time_step_fluid = project_parameters["fluid_solver_settings"]["solver_settings"]["time_stepping"]["time_step"].GetDouble()
            if time_step_structure != time_step_fluid:
                if (KratosMPI.mpi.rank == 0) : raise("ERROR: Different time step among subdomains! No sub-stepping implemented yet.")

        self.time_step = time_step_fluid

        # Take the each one of the solvers settings from the ProjectParameters
        self.settings = KratosMultiphysics.Parameters("{}")
        self.settings.AddValue("structure_solver_settings",project_parameters["structure_solver_settings"]["solver_settings"])
        self.settings.AddValue("fluid_solver_settings",project_parameters["fluid_solver_settings"]["solver_settings"])
        self.settings.AddValue("coupling_solver_settings",project_parameters["coupling_solver_settings"]["solver_settings"])
        self.settings.AddValue("mapper_settings",project_parameters["coupling_solver_settings"]["mapper_settings"])

        # Overwrite the default settings with user-provided parameters
        self.settings.RecursivelyValidateAndAssignDefaults(default_settings)

        # Auxiliar variables
        self.max_nl_it = self.settings["coupling_solver_settings"]["nl_max_it"].GetInt()
        self.nl_tol = self.settings["coupling_solver_settings"]["nl_tol"].GetDouble()
        self.solve_mesh_at_each_iteration = self.settings["coupling_solver_settings"]["solve_mesh_at_each_iteration"].GetBool()
        self.coupling_algorithm = self.settings["coupling_solver_settings"]["coupling_scheme"].GetString()
        self.fluid_interface_submodelpart_name = self.settings["coupling_solver_settings"]["fluid_interfaces_list"][0].GetString()
        self.structure_interface_submodelpart_name = self.settings["coupling_solver_settings"]["structure_interfaces_list"][0].GetString()
        coupling_utility_parameters = self.settings["coupling_solver_settings"]["coupling_strategy"]

        # Construct the structure solver
        structure_solver_module = __import__(self.settings["structure_solver_settings"]["solver_type"].GetString())
        self.structure_solver = structure_solver_module.CreateSolver(self.structure_main_model_part,
                                                                     self.settings["structure_solver_settings"])
        if (KratosMPI.mpi.rank == 0) : print("* Structure solver constructed.")

        # Construct the fluid solver
        self.fluid_solver = python_solvers_wrapper_fluid.CreateSolver(self.fluid_main_model_part,
                                                                      project_parameters["fluid_solver_settings"])
        if (KratosMPI.mpi.rank == 0) : print("* Fluid solver constructed.")

        # Construct the coupling partitioned strategy
        import convergence_accelerator_factory
        self.coupling_utility = convergence_accelerator_factory.CreateTrilinosConvergenceAccelerator(coupling_utility_parameters)
        if (KratosMPI.mpi.rank == 0) : print("* Coupling strategy constructed.")

        # Construct the ALE mesh solver
        mesh_solver_settings = KratosMultiphysics.Parameters("{}")
        mesh_solver_settings.AddValue("mesh_reform_dofs_each_step",self.settings["coupling_solver_settings"]["mesh_reform_dofs_each_step"])

        self.mesh_solver_module = __import__(self.settings["coupling_solver_settings"]["mesh_solver"].GetString())
        self.mesh_solver = self.mesh_solver_module.CreateSolver(self.fluid_solver.main_model_part,
                                                                mesh_solver_settings)
        if (KratosMPI.mpi.rank == 0):
            print("* ALE mesh solver constructed.")
            print("** Partitioned FSI base solver constructed.")


    # FROM BASE SOLVER, TODO: should this be return max()?¿?¿?¿
    # def GetMinimumBufferSize(self):
    #     # Get structure buffer size
    #     buffer_structure = self.structure_solver.GetMinimumBufferSize()
    #     # Get fluid buffer size
    #     buffer_fluid = self.fluid_solver.GetMinimumBufferSize()
    #
    #     return min(buffer_structure,buffer_fluid)


    def AddVariables(self):
        ## Structure variables addition
        # Standard CSM variables addition
        self.structure_solver.AddVariables()

        ## Fluid variables addition
        # Standard CFD variables addition
        self.fluid_solver.AddVariables()
        self.fluid_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.FORCE)
        self.fluid_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISPLACEMENT)
        # Mesh solver variables addition
        self.mesh_solver.AddVariables()

        ## FSIApplication variables addition
        # NonConformant_OneSideMap.AddVariables(self.fluid_solver.main_model_part,self.structure_solver.main_model_part) TODO: Add MAPPING app variables
        self.fluid_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.VECTOR_PROJECTED)
        self.fluid_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.FSI_INTERFACE_RESIDUAL)
        self.fluid_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.FSI_INTERFACE_MESH_RESIDUAL)
        self.structure_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.POSITIVE_MAPPED_VECTOR_VARIABLE)
        self.structure_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.NEGATIVE_MAPPED_VECTOR_VARIABLE)
        self.structure_solver.main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.VECTOR_PROJECTED)


    # FROM BASE SOLVER
    # def ImportModelPart(self):
    #     # Import structure model part
    #     self.structure_solver.ImportModelPart()
    #
    #     # Import fluid model part
    #     self.fluid_solver.ImportModelPart()


    # FROM BASE SOLVER
    # def AddDofs(self):
    #     # Add DOFs structure
    #     self.structure_solver.AddDofs()
    #
    #     # Add DOFs fluid
    #     self.fluid_solver.AddDofs()
    #     self.mesh_solver.AddDofs()


    # FROM BASE SOLVER
    # def Initialize(self):
    #     # Initialize fluid, structure and coupling solvers
    #     self.fluid_solver.SolverInitialize()
    #     self.structure_solver.InitializeStrategy()
    #     self.coupling_utility.Initialize()


    # FROM BASE SOLVER
    # def InitializeSolutionStep(self):
    #     # Initialize solution step of fluid, structure and coupling solvers
    #     self.fluid_solver.SolverInitializeSolutionStep()
    #     self.structure_solver.InitializeSolutionStep()
    #     self.coupling_utility.InitializeSolutionStep()


    # FROM BASE SOLVER
    # def Predict(self):
    #     # Perform fluid and structure solvers predictions
    #     self.fluid_solver.SolverPredict()
    #     self.structure_solver.Predict()


    # FROM BASE SOLVER
    # def ComputeDeltaTime(self):
    #     return self.time_step


    # FROM BASE SOLVER
    # def Solve(self):
    #     raise Exception("Calling the partitioned FSI base solver Solve() method.\n Please implement the custom Initialize() method for your scheme (e.g. Dirichlet-Neumann).")


    # FROM BASE SOLVER
    # def SetEchoLevel(self, structure_echo_level, fluid_echo_level):
    #     self.structure_solver.SetEchoLevel(self, structure_echo_level)
    #     self.fluid_solver.SetEchoLevel(self, fluid_echo_level)


    # FROM BASE SOLVER
    # def SetTimeStep(self, step):
    #     self.fluid_solver.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.TIME_STEPS, step)
    #     self.structure_solver.main_model_part.ProcessInfo.SetValue(KratosMultiphysics.TIME_STEPS, step)


    # FROM BASE SOLVER
    # def Clear(self):
    #     self.fluid_solver.Clear()
    #     self.structure_solver.Clear()


    # FROM BASE SOLVER
    # def Check(self):
    #     self.fluid_solver.Check()
    #     self.structure_solver.Check()


    #######################################################################
    ##############          PRIVATE METHODS SECTION          ##############
    #######################################################################

    ### AUXILIAR METHODS ###
    # FROM BASE SOLVER
    # def _GetFluidInterfaceSubmodelPart(self):
    #     # Returns the fluid interface submodelpart that will be used in the residual minimization
    #     return self.fluid_solver.main_model_part.GetSubModelPart(self.fluid_interface_submodelpart_name)


    # FROM BASE SOLVER
    # def _GetStructureInterfaceSubmodelPart(self):
    #     # Returns the structure interface submodelpart that will be used in the residual minimization
    #     return self.structure_solver.main_model_part.GetSubModelPart(self.structure_interface_submodelpart_name)


    # FROM BASE SOLVER
    # def _GetDomainSize(self):
    #
    #     fluid_domain_size = self.fluid_solver.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE]
    #     structure_domain_size = self.structure_solver.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE]
    #
    #     if fluid_domain_size !=structure_domain_size:
    #         raise("ERROR: Solid domain size and fluid domain size are not equal!")
    #
    #     return fluid_domain_size


    def _GetPartitionedFSIUtilities(self):

        if (self.domain_size == 2):
            return KratosTrilinos.TrilinosPartitionedFSIUtilities2D(self.epetra_communicator)
        else:
            return KratosTrilinos.TrilinosPartitionedFSIUtilities3D(self.epetra_communicator)

    ### TODO: SUBSTITUTE IN THIS METHOD THE OLD MAPPER BY THE ONE IN THE FSI APPLICATION
    def _SetUpMapper(self):

        # Recall, to set the INTERFACE flag in both the fluid and solid interface before the mapper construction
        # Currently this is done with the FSI application Python process set_interface_process.py
        # TODO: SINCE WE HAVE SUBMODELPARTS, TO SET THE INTERFACE FLAG SEEMS TO NOT BE STRICKLY NECESSARY
        search_radius_factor = 2.0
        mapper_max_iterations = 200
        mapper_tolerance = 1e-12

        if (self.settings["mapper_settings"].size() == 1):
            fluid_submodelpart_name = self.settings["mapper_settings"][0]["fluid_interface_submodelpart_name"].GetString()
            structure_submodelpart_name = self.settings["mapper_settings"][0]["structure_interface_submodelpart_name"].GetString()

            project_parameters_mapper = KratosMultiphysics.Parameters("{}")
            project_parameters_mapper.AddEmptyValue("mapper_type").SetString("NearestElement")
            project_parameters_mapper.AddEmptyValue("interface_submodel_part_origin").SetString(fluid_submodelpart_name)
            project_parameters_mapper.AddEmptyValue("interface_submodel_part_destination").SetString(structure_submodelpart_name)

            self.interface_mapper = KratosMapping.MapperFactory(self.fluid_solver.main_model_part,
				                                                self.structure_solver.main_model_part,
				                                                project_parameters_mapper)

            self.double_faced_structure = False

        elif (self.settings["mapper_settings"].size() == 2):
            # Get the fluid interface faces submodelpart names
            for mapper_id in range(2):
                if (self.settings["mapper_settings"][mapper_id]["mapper_face"].GetString() == "Positive"):
                    pos_face_submodelpart_name = self.settings["mapper_settings"][mapper_id]["fluid_interface_submodelpart_name"].GetString()
                elif (self.settings["mapper_settings"][mapper_id]["mapper_face"].GetString() == "Negative"):
                    neg_face_submodelpart_name = self.settings["mapper_settings"][mapper_id]["fluid_interface_submodelpart_name"].GetString()
                else:
                    raise Exception("Unique mapper flag has been set but more than one mapper exist in mapper_settings.")
            # Get the structure submodelpart name
            structure_submodelpart_name = self.settings["mapper_settings"][0]["structure_interface_submodelpart_name"].GetString()

            # Grab the interface submodelparts
            pos_fluid_submodelpart = self.fluid_solver.main_model_part.GetSubModelPart(pos_face_submodelpart_name)
            neg_fluid_submodelpart = self.fluid_solver.main_model_part.GetSubModelPart(neg_face_submodelpart_name)
            structure_submodelpart = self.structure_solver.main_model_part.GetSubModelPart(structure_submodelpart_name)




            # TODO: SET THE DOUBLE SIDE SURFACE MAPPING

            # self.interface_mapper = NonConformant_OneSideMap.NonConformantTwoFaces_OneSideMap(pos_fluid_submodelpart,
            #                                                                                   neg_fluid_submodelpart,
            #                                                                                   structure_submodelpart,
            #                                                                                   search_radius_factor,
            #                                                                                   mapper_max_iterations,
            #                                                                                   mapper_tolerance)

            # TODO: SET THE DOUBLE SIDE SURFACE MAPPING




            self.double_faced_structure = True

        else:
            raise Exception("Case with more than 2 mappers has not been implemented yet.\n \
                             Please, in case you are using single faced immersed bodies, set the skin entities in a unique submodelpart.\n \
                             In case you are considering double faced immersed bodies (shells or membranes), set all the positive faces \
                             in a unique submodelpart and all the negative ones in another submodelpart.")


     # FROM BASE SOLVER
    # def _SetStructureNeumannCondition(self):
    #
    #     structure_computational_submodelpart = self.structure_solver.GetComputingModelPart()
    #
    #     aux_count = 0
    #     for cond in self.structure_solver.main_model_part.Conditions:
    #         if(cond.Id > aux_count):
    #             aux_count = cond.Id
    #
    #     for i in range(self.settings["coupling_solver_settings"]["structure_interfaces_list"].size()):
    #         interface_submodelpart_name = self.settings["coupling_solver_settings"]["structure_interfaces_list"][i].GetString()
    #         interface_submodelpart_i = self.structure_solver.main_model_part.GetSubModelPart(interface_submodelpart_name)
    #         # NOTE: In this manner, two interface submodelparts cannot share a node (it would be repeated in the pointload conditions...)
    #
    #         # Create the point load condition
    #         if self.domain_size == 2:
    #             for node in interface_submodelpart_i.Nodes:
    #                 aux_count+=1
    #                 structure_computational_submodelpart.CreateNewCondition("PointLoadCondition2D1N",aux_count,[node.Id],self.structure_solver.main_model_part.Properties[0])
    #
    #         elif self.domain_size == 3:
    #             for node in interface_submodelpart_i.Nodes:
    #                 aux_count+=1
    #                 structure_computational_submodelpart.CreateNewCondition("PointLoadCondition3D1N",aux_count,[node.Id],self.structure_solver.main_model_part.Properties[0])


    # TODO: This function must be checked as soon as the fluid Neumann BC has been implemented.
    # FROM BASE SOLVER
    # def _SetFluidNeumannCondition(self):
    #
    #     fluid_computational_volume_submodelpart = self.fluid_solver.GetComputingModelPart()
    #
    #     aux_count = len(self.fluid_solver.main_model_part.Conditions)       # Get the last existing condition numbering
    #     aux_count += 1
    #     print("max aux_count",aux_count)
    #     aux_count = 0
    #     for cond in self.fluid_solver.main_model_part.Conditions:
    #         if(cond.Id > aux_count):
    #             aux_count = cond.Id
    #     aux_count += 1
    #     print("max aux_count",aux_count)
    #
    #
    #     for i in range(self.settings["coupling_solver_settings"]["fluid_interfaces_list"].size()):
    #         interface_submodelpart_name = self.settings["coupling_solver_settings"]["fluid_interfaces_list"][i].GetString()
    #         interface_submodelpart_i = self.fluid_solver.main_model_part.GetSubModelPart(interface_submodelpart_name)
    #         # NOTE: In this manner, two interface submodelparts cannot share a node (it would be repeated in the pointload conditions...)
    #         # DO CreateNewCondition CHECK IF THERE EXIST A CONDITION IN A NODE?
    #
    #         for node in interface_submodelpart_i.Nodes:
    #
    #             # NOTE: THIS CONDITION REMAINS TO BE IMPLEMENTED IN THE FluidDynamicsApplication, DECIDE WHAT TO DO.
    #             # Create the fluid load condition
    #             if self.fluid_solver.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 2:
    #                 fluid_computational_volume_submodelpart.CreateNewCondition("PointForce2Dfluid",aux_count,[node.Id],self.fluid_solver.main_model_part.Properties[0])
    #             elif self.structure_solver.main_model_part.ProcessInfo[KratosMultiphysics.DOMAIN_SIZE] == 3:
    #                 fluid_computational_volume_submodelpart.CreateNewCondition("PointForce3Dfluid",aux_count,[node.Id],self.fluid_solver.main_model_part.Properties[0])
    #
    #             aux_count+=1


    # TODO: GET IT FROM THE SERIAL BASE SOLVER ONCE THE MAPPER IN MAPPING APPLICATION IS USED IN SERIAL PROBLEMS AS WELL
    def _ComputeMeshPredictionSingleFaced(self):

            if (KratosMPI.mpi.rank == 0) : print("Computing time step ",self.fluid_solver.main_model_part.ProcessInfo[KratosMultiphysics.TIME_STEPS]," prediction...")
            # Get the previous step fluid interface nodal fluxes
            self.interface_mapper.Map(KratosMultiphysics.REACTION,
                                      KratosStructural.POINT_LOAD,
                                      KratosMapping.MapperFactory.SWAP_SIGN |
                                      KratosMapping.MapperFactory.CONSERVATIVE)

            # Solve the current step structure problem with the previous step fluid interface nodal fluxes
            self.structure_solver.SolveSolutionStep()

            # Map the obtained structure displacement to the fluid interface
            #TODO: CHECK THE VARIABLES ORDER IN MAPPING
            # self.interface_mapper.InverseMap(KratosMultiphysics.DISPLACEMENT,
            #                                  KratosMultiphysics.MESH_DISPLACEMENT)
            self.interface_mapper.InverseMap(KratosMultiphysics.MESH_DISPLACEMENT,
                                             KratosMultiphysics.DISPLACEMENT)

            # Solve the mesh problem
            self.mesh_solver.Solve()

            if (KratosMPI.mpi.rank == 0) : print("Mesh prediction computed.")


    # FROM BASE SOLVER
    # def _ComputeMeshPredictionDoubleFaced(self):
    #
    #         print("Computing time step ",self.fluid_solver.main_model_part.ProcessInfo[KratosMultiphysics.TIME_STEPS],"double faced prediction...")
    #         # Get the previous step fluid interface nodal fluxes from both positive and negative faces
    #         keep_sign = False
    #         distribute_load = True
    #         self.interface_mapper.PositiveFluidToStructure_VectorMap(KratosMultiphysics.REACTION,
    #                                                                  KratosFSI.POSITIVE_MAPPED_VECTOR_VARIABLE,
    #                                                                  keep_sign,
    #                                                                  distribute_load)
    #         self.interface_mapper.NegativeFluidToStructure_VectorMap(KratosMultiphysics.REACTION,
    #                                                                  KratosFSI.NEGATIVE_MAPPED_VECTOR_VARIABLE,
    #                                                                  keep_sign,
    #                                                                  distribute_load)
    #
    #         # Add the two faces contributions to the POINT_LOAD variable
    #         # TODO: Add this to the variables utils
    #         for node in self._GetStructureInterfaceSubmodelPart().Nodes:
    #             pos_face_force = node.GetSolutionStepValue(KratosFSI.POSITIVE_MAPPED_VECTOR_VARIABLE)
    #             neg_face_force = node.GetSolutionStepValue(KratosFSI.NEGATIVE_MAPPED_VECTOR_VARIABLE)
    #             node.SetSolutionStepValue(KratosStructural.POINT_LOAD, 0, pos_face_force+neg_face_force)
    #
    #         # Solve the current step structure problem with the previous step fluid interface nodal fluxes
    #         self.structure_solver.SolveSolutionStep()
    #
    #         # Map the obtained structure displacement to both positive and negative fluid interfaces
    #         keep_sign = True
    #         distribute_load = False
    #         self.interface_mapper.StructureToPositiveFluid_VectorMap(KratosMultiphysics.DISPLACEMENT,
    #                                                                  KratosMultiphysics.MESH_DISPLACEMENT,
    #                                                                  keep_sign,
    #                                                                  distribute_load)
    #         self.interface_mapper.StructureToNegativeFluid_VectorMap(KratosMultiphysics.DISPLACEMENT,
    #                                                                  KratosMultiphysics.MESH_DISPLACEMENT,
    #                                                                  keep_sign,
    #                                                                  distribute_load)
    #
    #         # Solve the mesh problem
    #         self.mesh_solver.Solve()
    #
    #         print("Mesh prediction computed.")