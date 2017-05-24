﻿from __future__ import print_function, absolute_import, division

import KratosMultiphysics.KratosUnittest as KratosUnittest
import KratosMultiphysics

import os
import sys


def GetFilePath(fileName):
    return os.path.dirname(os.path.realpath(__file__)) + "/" + fileName


class TestModelPartIO(KratosUnittest.TestCase):

    def setUp(self):
        if (sys.version_info < (3, 2)):
            self.assertRaisesRegex = self.assertRaisesRegexp

    def test_reorder(self):
        model_part = KratosMultiphysics.ModelPart("Main")
        model_part.CreateNewNode(1,0,0,0)
        model_part.CreateNewNode(2,1,0,0)                
        model_part.CreateNewNode(3,2,0,0)
        model_part.CreateNewNode(4,3,0,0)
        model_part.CreateNewNode(5,0,1,0)
        model_part.CreateNewNode(6,1,1,0)
        model_part.CreateNewNode(7,2,1,0)
        model_part.CreateNewNode(8,3,1,0)
        model_part.CreateNewNode(9,0,2,0)
        model_part.CreateNewNode(10,1,2,0)
        model_part.CreateNewNode(11,2,2,0)
        model_part.CreateNewNode(12,3,2,0)        
        #nodes are numbered as
        #9 10 11 12
        #5 6  7  8
        #1 2  3  4
        model_part.CreateNewElement("Element2D4N",1,[1,2,6,5], model_part.GetProperties()[1])
        model_part.CreateNewElement("Element2D4N",2,[2,3,7,6], model_part.GetProperties()[1])
        model_part.CreateNewElement("Element2D4N",3,[3,4,8,7], model_part.GetProperties()[1])
        model_part.CreateNewElement("Element2D4N",4,[5,6,10,9], model_part.GetProperties()[1])
        model_part.CreateNewElement("Element2D4N",5,[6,7,11,10], model_part.GetProperties()[1])
        model_part.CreateNewElement("Element2D4N",6,[7,8,12,11], model_part.GetProperties()[1])
        
        tmp = KratosMultiphysics.Parameters("{}")
        KratosMultiphysics.ReorderAndOptimizeModelPartProcess(model_part,tmp).Execute()
        
        #output is
        #10 11 12 9
        #6   7  4 8
        #1   2  3 5

        
        for node in model_part.Nodes:
            print(node.Id, node.X,node.Y)
            
        for elem in model_part.Elements:
            tmp = []
            for node in elem.GetNodes():
                tmp.append(node.Id)
            print(elem.Id,tmp)


if __name__ == '__main__':
    KratosUnittest.main()
