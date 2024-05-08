# dvtool_testcases_manage
this is a toolkit for dv testcases management, tc is short for testcase. 
## Features:
1. Records the properties of each test case
2. Each testcase is a block created by testcase... end 
3. Each testcase contains three stages of attribute parameters, include pre cfgs stage, simulation stage,and post simulation stage, which are as described in the Attribute section
4. pre_cfgs_when and simg_args_value can extend by father testcase block. If the testcase's pre_cfgs_type='testcase' , the pre_cfgs_value means fater testcase , the test can extend fater testcase's pre_cfgs and simg_args.

## Data structure
### single testcase
```
testcase = {  
                'pre_cfgs_name':   [],  
                'pre_cfgs_type':   [],  
                'pre_cfgs_value':  [],  
                'pre_cfgs_when':   [],  
                'sim_args_value':  [],  
                'post_cfgs_value': []  
            }  
```
### multiple testcases
```
testcases1 = {  
                'testcase_name':   [],  
                'testcase_type':   [],  
                'testcase_value':  [],  
                'testcase_when':   [],  
                'testcase_simg_args_value':  [],  
                'testcase_post_cfgs_value': []  
            }
testcases2 = {  
                'testcase_name':   [],  
                'testcase_type':   [],  
                'testcase_value':  [],  
                'testcase_when':   [],  
                'testcase_simg_args_value':  [],  
                'testcase_post_cfgs_value': []  
            }
final_testcases = [testcases1, testcases2]
```
## Attributes:
### [pre_cfgs]  
1. [pre_cfgs].name  this is a name for the simulation testcase 
2. [pre_cfgs].type  this is a type for tc configuration, it can be template or a testcase
* template  if this "type" is "template" the testcase will not publish , it only provide shared values,  who extend this testcase , it will get the shared attributes include pre_cfgs and sim_args and post_cfgs
* if this "type" is "testcase" the testcase will be published and can be run by testrunner testcase  if this "type" is "clone" the testcase will be published and can be run 
1. [pre_cfgs].value it will define some options in pre_cfgs, it can be a string. every options will only have one line
2. [pre_cfgs].when  it means regression tag, user can define multiple tags, it will be used to filter testcases when kick off regression
        
### [sim_args] 
1. [sim_args].value this is a string, it will be used as a command line argument for simulation. dvrun scripts will publish it and format it
### [post_cfgs]
1. [post_cfgs].value this is a name for the post_cfgs, it will be used after simulation finished. it will be used for some post scripts 
## example:
```
testcase:      
    attribute[pre_cfgs].name="riscv_base_test"
    attribute[pre_cfgs].type="template"
    attribute[sim_args].value="-efgh_random_enable=10"
    attribute[sim_args].value="-efgh_random_disable=10"
end

testcase:      
    attribute[pre_cfgs].name="riscv_base_test_1"
    attribute[pre_cfgs].type="testcase"
    attribute[pre_cfgs].value="riscv_base_test"   
    attribute[pre_cfgs].when ="sanity"   
    attribute[sim_args].variant="riscv_base_tc"
    attribute[sim_args].value="-1_random_enable=50"
    attribute[sim_args].value="-1_random_disable=50"
end

testcase:      
    attribute[pre_cfgs].name="riscv_base_test_2"
    attribute[pre_cfgs].type="testcase"
    attribute[pre_cfgs].value="riscv_base_test_1"   
    attribute[pre_cfgs].when ="sanity"   
    attribute[sim_args].variant="riscv_base_tc"
    attribute[sim_args].value="-2_random_enable=50"
    attribute[sim_args].value="-2_random_disable=50"
end
```

## How to use it
```
    from test_case_manage import TC_management
    # initialize the tc_management class
    tc_management = TC_management()  
    # set template file path
    tc_management.set_file_path('test_template.j2')
    # get the tc_dict_list block (it will return a list)
    tc_dict_list = tc_management.attribute_resolver()
    # get the testcase dict list select by regr_tags
    tc_dict_list = tc_management.select_test_by_regrTags("sanity")
    # get the testcase dict list select by variant
    tc_dict_list = tc_management.select_test_by_regrtestNames( "riscv_base_test_2")


```
# Checking
 [pre_cfgs] 
   if pre_cfgs.type is "testcase" , the next line must be pre_cfgs.value it means ,this testcase is extended from 
   another testcase, the pre_cfgs.value is the name of the extended testcase
