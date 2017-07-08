//
//   Project Name:        KratosFemToDemApplication $
//   Created by:          $Author:Alejandro Cornejo $
//   Last modified by:    $Co-Author:                     $
//   Date:                $Date:                Sept 2016 $
//   Revision:            $Revision:                  0.0 $
//
//

#include "fem_to_dem_application_variables.h"

namespace Kratos
{
	KRATOS_CREATE_VARIABLE(double, DAMAGE_EDGE1)
	KRATOS_CREATE_VARIABLE(double, DAMAGE_EDGE2)
	KRATOS_CREATE_VARIABLE(double, DAMAGE_EDGE3)
	KRATOS_CREATE_VARIABLE(double, DAMAGE_ELEMENT)
	KRATOS_CREATE_VARIABLE(Vector,STRESS_VECTOR)
	KRATOS_CREATE_VARIABLE(double, YIELD_STRESS_C)
	KRATOS_CREATE_VARIABLE(double, YIELD_STRESS_T)
	KRATOS_CREATE_VARIABLE(int, ITER)
	KRATOS_CREATE_VARIABLE(double, FRAC_ENERGY_T)
	KRATOS_CREATE_VARIABLE(double, FRAC_ENERGY_C)
	KRATOS_CREATE_VARIABLE(Vector, STRESS_VECTOR_INTEGRATED)
	KRATOS_CREATE_VARIABLE(double, THRESHOLD)
	KRATOS_CREATE_VARIABLE(Vector, SMOOTHED_STRESS_VECTOR)
	KRATOS_CREATE_VARIABLE(std::string,YIELD_SURFACE)
	KRATOS_CREATE_VARIABLE(Vector, STRAIN_VECTOR)
	KRATOS_CREATE_VARIABLE(bool, TANGENT_CONSTITUTIVE_TENSOR)
	KRATOS_CREATE_VARIABLE(bool, SMOOTHING)
	
}
