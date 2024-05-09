
import re


class TC_toolkit(object):
    def __init__(self) -> None:
        self.path=''
    def set_file_path(self,path):
        self.path=path
    def get_file_path(self):
        return self.path
    def read_file(self):  
        file_path = self.get_file_path()  
        with open(file_path, 'r') as file:  
            return file.readlines() 
class TC_management(TC_toolkit):
    def __init__(self) -> None:
        super().__init__()
    def get_import_tc(self):
       pass 
    def get_testblock(self):
        tc_block_list = []    
        testcase = False  
        current_block = []  
        for line in self.read_file():  
            line = line.strip()  
            if not line or line.startswith('#'):   
                continue  
            if line.startswith('testcase:'):  
                if testcase:  
                    if current_block:  
                        tc_block_list.append(''.join(current_block))  
                testcase = True  
                # 去除 testcase: 前缀，并添加当前行（不带前缀和换行符）到 current_block  
                current_block = [line[len('testcase:'):].strip()]  
            elif testcase and not line.startswith('end'):  
                current_block.append(line + '\n')  
            elif testcase and line.startswith('end'):  
                tc_block_list.append(''.join(current_block))  
                testcase = False  
                current_block = []  
        if testcase and current_block:  
            tc_block_list.append(''.join(current_block))  

        return tc_block_list  
    def attribute_resolver(self):
        tc_dict_list=[]
        tc_block=self.get_testblock()
        for tc in tc_block:
            tmp_dict = {  
                'pre_cfgs_name':   [],  
                'pre_cfgs_type':   [],  
                'pre_cfgs_value':  [],  
                'pre_cfgs_when':   [],  
                'sim_args_value':  [],  
                'post_cfgs_value': []  
            }  
            for line in tc.split('\n'):
                if self.get_attribute_type(line) == 'pre_cfgs_name':  
                    tmp_dict['pre_cfgs_name'].append(self.get_attribute_data(line))  
                elif self.get_attribute_type(line) == 'pre_cfgs_type':  
                    tmp_dict['pre_cfgs_type'].append(self.get_attribute_data(line))  
                elif self.get_attribute_type(line) == 'pre_cfgs_value':  
                    tmp_dict['pre_cfgs_value'].append(self.get_attribute_data(line))  
                elif self.get_attribute_type(line) == 'pre_cfgs_when':  
                    tmp_dict['pre_cfgs_when'].append(self.get_attribute_data(line))  
                elif self.get_attribute_type(line) == 'sim_args_value':  
                    tmp_dict['sim_args_value'].append(self.get_attribute_data(line))  
                elif self.get_attribute_type(line) == 'post_cfgs_value':  
                    tmp_dict['post_cfgs_value'].append(self.get_attribute_data(line))
            tc_dict_list.append(tmp_dict.copy())
        
        return tc_dict_list
    def get_attribute_type(self,input_string):
        '''
        return atttribute type
        '''
        precfgs_name_pattern = re.compile(r'attribute\[pre_cfgs\]\.name\s*=\s*([^;\s]+)')  
        precfgs_type_pattern = re.compile(r'attribute\[pre_cfgs\]\.type\s*=\s*([^;\s]+)')  
        precfgs_value_pattern = re.compile(r'attribute\[pre_cfgs\]\.value\s*=\s*([^;\s]+)')  
        precfgs_when_pattern = re.compile(r'attribute\[pre_cfgs\]\.when\s*=\s*([^;\s]+)')  
        simargs_value_pattern = re.compile(r'attribute\[sim_args\]\.value\s*=\s*([^;\s]+)')  
        postcfgs_value_pattern = re.compile(r'attribute\[post_cfgs\]\.value\s*=\s*([^;\s]+)')  

        precfgs_name_match = precfgs_name_pattern.search(input_string)  
        if precfgs_name_match:  
            return 'pre_cfgs_name'  

        precfgs_type_match = precfgs_type_pattern.search(input_string)  
        if precfgs_type_match:  
            return 'pre_cfgs_type'  
        
        precfgs_value_match = precfgs_value_pattern.search(input_string)
        if precfgs_value_match:
            return 'pre_cfgs_value'
        
        precfgs_when_match = precfgs_when_pattern.search(input_string)
        if precfgs_when_match:
            return 'pre_cfgs_when'
        
        simargs_value_match = simargs_value_pattern.search(input_string)
        if simargs_value_match:
            return 'sim_args_value'
        
        postcfgs_value_match = postcfgs_value_pattern.search(input_string)
        if postcfgs_value_match:
            return 'post_cfgs_value'

        return None    
    def get_attribute_data(self, input_string):  
        '''
        return attribute data
        '''
        pattern = r'=(["\'])(.*?)\1' 
        match = re.search(pattern, input_string)  
        if match:  
            value = match.group(2) 
            return value
        return None
    

    def select_test_by_regrTags(self, regr_tag):  
        select_test_by_regrTags = []  
        seen_dicts = set()     
        test_dict_list = self.attribute_resolver()  
        test_dict_list=self.extend_sim_args(test_dict_list)
        
        for test_dict in test_dict_list:  
            if any(regr_tag_item in test_dict['pre_cfgs_when'] for regr_tag_item in regr_tag):  
                key = tuple(test_dict['pre_cfgs_name']) if test_dict['pre_cfgs_name'] else None    
                if key not in seen_dicts:  
                    select_test_by_regrTags.append(test_dict)  
                    seen_dicts.add(key)  
        return select_test_by_regrTags
    def select_test_by_testNames(self,test_names):
        select_test_by_testNames = []
        test_dict_list = self.attribute_resolver()  
        test_dict_list=self.extend_sim_args(test_dict_list)
        for test_dict in test_dict_list:
            if test_dict['pre_cfgs_name'][0] in test_names:
                select_test_by_testNames.append(test_dict)

        return select_test_by_testNames
    def extend_sim_args(self,test_cases):  
        for testcase in test_cases:
            current_sim_args=[]
            current_pre_cfgs_when=[]
            if testcase['pre_cfgs_type'][0]=='template':
                need_to_extend=False
                continue
            else:
                need_to_extend=True
            current_pre_cfgs_value=testcase['pre_cfgs_value'][0]
            current_sim_args.extend(testcase['sim_args_value'])
            current_pre_cfgs_when.extend(testcase['pre_cfgs_when'])
            while  need_to_extend:
                for tc in test_cases :
                    if(tc['pre_cfgs_name'][0]==current_pre_cfgs_value):
                        current_sim_args.extend(tc['sim_args_value'])
                        current_pre_cfgs_when.extend(tc['pre_cfgs_when'])
                        if (tc['pre_cfgs_type'][0]=='template'):
                            need_to_extend=False
                        else:
                            current_pre_cfgs_value=tc['pre_cfgs_value'][0]
            testcase['sim_args_value']=list(set(current_sim_args))
            testcase['pre_cfgs_when']=list(set(current_pre_cfgs_when))

        return test_cases
                    
    

def main():
    tc_management = TC_management()  
    tc_management.set_file_path('test_template.j2')
    tc_block_list = tc_management.get_testblock()  
    for tc_block in tc_block_list:  
        print(tc_block)
    
    tc_dict_list = tc_management.attribute_resolver()
    for tc_dict in tc_dict_list:
        print(tc_dict)
        print(tc_dict['pre_cfgs_name'])

    regr_tag=['sanity']
    print ("sanity:")
    print(tc_management.select_test_by_regrTags(regr_tag))
    print("-------------------------------------------------------------")
    regr_tag=['base']
    print ("base:")
    print(tc_management.select_test_by_regrTags(regr_tag))
    print("-------------------------------------------------------------")
    regr_tag=['sanity','base']
    print ("sanity+base:")
    print(tc_management.select_test_by_regrTags(regr_tag))
    print("-------------------------------------------------------------")

if __name__ == '__main__':
    main()