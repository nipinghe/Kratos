//    |  /           |
//    ' /   __| _` | __|  _ \   __|
//    . \  |   (   | |   (   |\__ `
//   _|\_\_|  \__,_|\__|\___/ ____/
//                   Multi-Physics
//
//   License:        BSD License
//   Kratos default license: kratos/license.txt
//
//   Project Name:        $StructuralMechanicsApplication $
//   Last modified by:    $Author:	 peter.wilson@tum.de  $
//   Date:                $Date:     May 2017		      $
//   Revision:            $Revision: 0.0				  $

#if !defined(KRATOS_EIGENSOLVER_STABILITY_SCHEME )
#define  KRATOS_EIGENSOLVER_STABILITY_SCHEME


// System includes

// External includes

// Project includes
#include "includes/define.h"
#include "includes/element.h"
#include "includes/condition.h"
#include "includes/process_info.h"
#include "includes/ublas_interface.h"
#include "solving_strategies/schemes/scheme.h"

// Application includes
#include "structural_mechanics_application_variables.h"

namespace Kratos
{

///@name Kratos Globals
///@{

///@}
///@name Type Definitions
///@{

///@}

///@name  Enum's
///@{

///@}
///@name  Functions
///@{

///@}
///@name Kratos Classes
///@{

/// An adapter scheme for obtaining material and geometric stiffness matrices for stability eigenvalue problems.
template<class TSparseSpace,
         class TDenseSpace
         >
class EigensolverStabilityScheme : public Scheme<TSparseSpace,TDenseSpace>
{
public:
    ///@name Type Definitions
    ///@{

    KRATOS_CLASS_POINTER_DEFINITION( EigensolverStabilityScheme );

    typedef Scheme<TSparseSpace,TDenseSpace> BaseType;

    typedef typename BaseType::LocalSystemVectorType LocalSystemVectorType;

    typedef typename BaseType::LocalSystemMatrixType LocalSystemMatrixType;

    ///@}
    ///@name Life Cycle
    ///@{

    /// Constructor.
    EigensolverStabilityScheme() : Scheme<TSparseSpace,TDenseSpace>() {}

    /// Destructor.
    virtual ~EigensolverStabilityScheme() {}

    ///@}
    ///@name Operators
    ///@{

    ///@}
    ///@name Operations
    ///@{

    virtual void CalculateSystemContributions(
        Element::Pointer pCurrentElement,
        LocalSystemMatrixType& LHS_Contribution,
        LocalSystemVectorType& RHS_Contribution,
        Element::EquationIdVectorType& EquationId,
        ProcessInfo& CurrentProcessInfo
    )
    {
		KRATOS_TRY

		CurrentProcessInfo[IS_STABILITY_EIGENPROBLEM] = true;

			if (CurrentProcessInfo[BUILD_LEVEL] == 1)
			{ // geometric stiffness matrix
				//std::cout << "---------- Geometric stiffness matrix called ----------" << std::endl;
				pCurrentElement->CalculateGeometricStiffnessMatrix(LHS_Contribution, CurrentProcessInfo);
				auto LocalSize = LHS_Contribution.size1();
				if (RHS_Contribution.size() != LocalSize)
					RHS_Contribution.resize(LocalSize, false);
				noalias(RHS_Contribution) = ZeroVector(LocalSize);
			}
			else if (CurrentProcessInfo[BUILD_LEVEL] == 2) // material stiffness matrix
            pCurrentElement->CalculateLocalSystem(LHS_Contribution,RHS_Contribution,CurrentProcessInfo);
        else
            KRATOS_THROW_ERROR(std::logic_error, "Invalid BUILD_LEVEL", "");

        pCurrentElement->EquationIdVector(EquationId,CurrentProcessInfo);

        KRATOS_CATCH("")
    }

    virtual void Calculate_LHS_Contribution(
        Element::Pointer pCurrentElement,
        LocalSystemMatrixType& LHS_Contribution,
        Element::EquationIdVectorType& EquationId,
        ProcessInfo& CurrentProcessInfo)
    {
        KRATOS_TRY

        LocalSystemVectorType RHS_Contribution;
        RHS_Contribution.resize(LHS_Contribution.size1(), false);
        CalculateSystemContributions(
                pCurrentElement,
                LHS_Contribution,
                RHS_Contribution,
                EquationId,
                CurrentProcessInfo);

        KRATOS_CATCH("")
    }

    virtual void Condition_CalculateSystemContributions(
        Condition::Pointer pCurrentCondition,
        LocalSystemMatrixType& LHS_Contribution,
        LocalSystemVectorType& RHS_Contribution,
        Condition::EquationIdVectorType& EquationId,
        ProcessInfo& CurrentProcessInfo)
    {
        KRATOS_TRY

        if (CurrentProcessInfo[BUILD_LEVEL] == 1)
        { // geometric stiffness matrix
            //pCurrentCondition->CalculateGeometricStiffnessMatrix(LHS_Contribution,CurrentProcessInfo); // TODO p0 fix!
            auto LocalSize = LHS_Contribution.size1();
            if (RHS_Contribution.size() != LocalSize)
                RHS_Contribution.resize(LocalSize,false);
            noalias(RHS_Contribution) = ZeroVector(LocalSize);
        }
        else if (CurrentProcessInfo[BUILD_LEVEL] == 2) // stiffness matrix
            pCurrentCondition->CalculateLocalSystem(LHS_Contribution,RHS_Contribution,CurrentProcessInfo);
        else
            KRATOS_THROW_ERROR(std::logic_error, "Invalid BUILD_LEVEL", "");

        pCurrentCondition->EquationIdVector(EquationId,CurrentProcessInfo);

        KRATOS_CATCH("")
    }

    virtual void Condition_Calculate_LHS_Contribution(
            Condition::Pointer pCurrentCondition,
            LocalSystemMatrixType& LHS_Contribution,
            Condition::EquationIdVectorType& EquationId,
            ProcessInfo& CurrentProcessInfo)
    {
        KRATOS_TRY

        LocalSystemVectorType RHS_Contribution;
        RHS_Contribution.resize(LHS_Contribution.size1(), false);
        Condition_CalculateSystemContributions(
                pCurrentCondition,
                LHS_Contribution,
                RHS_Contribution,
                EquationId,
                CurrentProcessInfo);

        KRATOS_CATCH("")
    }

    ///@}
    ///@name Access
    ///@{

    ///@}
    ///@name Inquiry
    ///@{

    ///@}
    ///@name Friends
    ///@{

    ///@}

protected:
    ///@name Protected static Member Variables
    ///@{

    ///@}
    ///@name Protected member Variables
    ///@{

    ///@}
    ///@name Protected Operators
    ///@{

    ///@}
    ///@name Protected Operations
    ///@{

    ///@}
    ///@name Protected  Access
    ///@{

    ///@}
    ///@name Protected Inquiry
    ///@{

    ///@}
    ///@name Protected LifeCycle
    ///@{

    ///@}

private:
    ///@name Static Member Variables
    ///@{

    ///@}
    ///@name Member Variables
    ///@{

    ///@}
    ///@name Private Operators
    ///@{

    ///@}
    ///@name Private Operations
    ///@{

    ///@}
    ///@name Private  Access
    ///@{

    ///@}
    ///@name Private Inquiry
    ///@{

    ///@}
    ///@name Un accessible methods
    ///@{

    ///@}

}; /* Class Scheme */

///@}

///@name Type Definitions
///@{

///@}

}  /* namespace Kratos.*/

#endif /* KRATOS_EIGENSOLVER_STABILITY_SCHEME  defined */
