// KRATOS  ___|  |                   |                   |
//       \___ \  __|  __| |   |  __| __| |   |  __| _` | |
//             | |   |    |   | (    |   |   | |   (   | |
//       _____/ \__|_|   \__,_|\___|\__|\__,_|_|  \__,_|_| MECHANICS
//
//  License:		 BSD License
//					 license: StructuralMechanicsApplication/license.txt
//
//  Main authors:    Vicente Mataix Ferrándiz
// 

#if !defined(PROCESS_FACTORY_UTILITY_DEFINED )
#define  PROCESS_FACTORY_UTILITY_DEFINED

// System includes
#include <iostream>
#include <vector>
#include "boost/smart_ptr.hpp"
#include <boost/python.hpp>

// External includes

// Project includes
#include "contact_structural_mechanics_application_variables.h"
#include "contact_structural_mechanics_application.h"

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

/** @brief This is a experimental process factory utility
 */
class ProcessFactoryUtility
{
public:

    ///@name Type Definitions
    ///@{
    /// Counted pointer of ProcessFactoryUtility
    KRATOS_CLASS_POINTER_DEFINITION( ProcessFactoryUtility );

    typedef typename boost::python::object ObjectType;
    
    typedef typename boost::python::list     ListType;
    
    ///@}
    ///@name Life Cycle
    ///@{

    /// Default constructors
    ProcessFactoryUtility(){}
    
    ProcessFactoryUtility(ListType& ProcessesList)
    {
        for (unsigned int iProcess = 0; iProcess < len(ProcessesList); ++iProcess)
        {
            mProcesses.push_back(boost::python::extract<ObjectType>(ProcessesList[iProcess]));
        }
    }

    /// Destructor.
    ~ProcessFactoryUtility(){}

    ///@}
    ///@name Operators
    ///@{
    
    /// Assignment operator.
    
    ProcessFactoryUtility& operator=(ProcessFactoryUtility const& rOther)
    {
        mProcesses = rOther.mProcesses;

        return *this;
    }
    
    ///@}
    ///@name Operations
    ///@{
    
    /**
     * It add new process to the existing process list
     */

    void AddProcess(ObjectType& rProcess)
    {
        mProcesses.push_back(rProcess);
    }
    
    /**
     * It add new processes to the existing process list
     */

    void AddProcesses(ListType& ProcessesList)
    {
        for (unsigned int iProcess = 0; iProcess < len(ProcessesList); ++iProcess)
        {
            mProcesses.push_back(boost::python::extract<ObjectType>(ProcessesList[iProcess]));
        }
    }
    
    /**
     * It executes the ExecuteInitialize() from the list of processes
     */

    void ExecuteInitialize()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteInitialize")();
        }
    }
    
    /**
     * It executes the ExecuteBeforeSolutionLoop() from the list of processes
     */
        
    void ExecuteBeforeSolutionLoop()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteBeforeSolutionLoop")();
        }
    }
    
    /**
     * It executes the ExecuteInitializeSolutionStep() from the list of processes
     */
        
    void ExecuteInitializeSolutionStep()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteInitializeSolutionStep")();
        }
    }
    
    /**
     * It executes the ExecuteFinalizeSolutionStep() from the list of processes
     */
        
    void ExecuteFinalizeSolutionStep()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteFinalizeSolutionStep")();
        }
    }
    
    /**
     * It executes the ExecuteBeforeOutputStep() from the list of processes
     */
        
    void ExecuteBeforeOutputStep()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteBeforeOutputStep")();
        }
    }
    
    /**
     * It executes the ExecuteAfterOutputStep() from the list of processes
     */
        
    void ExecuteAfterOutputStep()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteAfterOutputStep")();
        }
    }
    
    /**
     * It executes the ExecuteFinalize() from the list of processes
     */
        
    void ExecuteFinalize()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("ExecuteFinalize")();
        }
    }
    
    /**
     * It executes the Clear() from the list of processes
     */
    
    void Clear()
    {
        for (unsigned int iProcess = 0; iProcess < mProcesses.size(); iProcess++)
        {
            mProcesses[iProcess].attr("Clear")();
        }
    }

    ///@}
    ///@name Access
    ///@{

    ///@}
    ///@name Flags
    ///@{
    
    ///@}
    ///@name Inquiry
    ///@{
    
    ///@}
    ///@name Input and output
    ///@{
    
    /// Turn back information as a string.

    virtual std::string Info() const
    {
        std::stringstream buffer;
        buffer << "ProcessFactoryUtility. Number of processes:" << mProcesses.size();
        return buffer.str();
    }

    /// Print information about this object.

    virtual void PrintInfo(std::ostream& rOStream) const
    {
        rOStream << "ProcessFactoryUtility. Number of processes:" << mProcesses.size();
    }

    /// Print object's data.

    virtual void PrintData(std::ostream& rOStream) const
    {
        rOStream << "ProcessFactoryUtility. Number of processes:" << mProcesses.size();
    }

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

    std::vector<ObjectType> mProcesses;  

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

    ///@}
    ///@name Serialization
    ///@{

    friend class Serializer;

    virtual void save(Serializer& rSerializer) const
    {
        // TODO: Fill if necessary
//         rSerializer.save("Processes", mProcesses);
    }

    virtual void load(Serializer& rSerializer)
    {
        // TODO: Fill if necessary
//         rSerializer.load("Processes", mProcesses);
    }
    
    ///@name Private Inquiry
    ///@{
    ///@}

    ///@name Unaccessible methods
    ///@{
    ///@}
}; // Class ProcessFactoryUtility 

///@}

///@name Type Definitions
///@{


///@}
///@name Input and output
///@{

/// input stream function
inline std::istream & operator >>(std::istream& rIStream,
                                  ProcessFactoryUtility& rThis);

/// output stream function

inline std::ostream & operator <<(std::ostream& rOStream,
                                  const ProcessFactoryUtility& rThis)
{
    rThis.PrintInfo(rOStream);
    rOStream << " : " << std::endl;
    rThis.PrintData(rOStream);

    return rOStream;
}

///@}

}  // namespace Kratos.

#endif // PROCESS_FACTORY_UTILITY_DEFINED  defined