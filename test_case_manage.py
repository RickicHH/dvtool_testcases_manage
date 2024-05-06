
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
    def attribute_resolver(self,attribute_type):
        tc_block=self.get_testblock()
        for tc in tc_block:
            for line in tc.split('\n'):
                if self.attribute_identifier(line)=='pre_cfgs_name':
                    pass
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
    

def main():
    tc_management = TC_management()  
    tc_management.set_file_path('test_template.j2')
    tc_block_list = tc_management.get_testblock()  
    for tc_block in tc_block_list:  
        print(tc_block)

if __name__ == '__main__':
    main()