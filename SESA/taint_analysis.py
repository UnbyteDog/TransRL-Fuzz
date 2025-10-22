class TaintAnalysis:
    def __init__(self):
        self.source = []
        self.sink = []
        self.sanitizer = []
        self.taint_flows = []
    
    class TaintSource:
        '''
        污染源：节点类型，变量名，路径，行数
        '''
        def __init__(self,note_type,variable_name,file_path,line_no):
            self.note_type = note_type
            self.variable_name = variable_name
            self.file_path = file_path
            self.line_no = line_no

    class TaintSink:
        '''
        汇聚点：函数名，类型，路径，行数
        '''
        def __init__(self,function_name,sink_type,file_path,line_no):
            self.function_name = function_name
            self.sink_type = sink_type
            self.file_path = file_path
            self.line_no = line_no
    
    class SanitizerPonit:
        #effectiveness 留一个净化效果等级
        '''
        净化点：函数名，净化类型，路径，行数，输入，输出
        '''
        def __init__(self,funciton_name,sanitizer_type,file_path,line_no,input_variable,output_variable):
            self.function_name = funciton_name
            self.sanitizer_type = sanitizer_type
            self.file_path = file_path
            self.line_no = line_no
            self.input_variable = input_variable
            self.output_variable = output_variable

    class PropagationPath:
        '''
        传播路径：污染源，汇聚点，（路径节点，净化节点）
        '''
        def __init__(self,source,sink,path_note=None,sanitizer_note=None):
            self.source = source
            self.sink = sink
            self.path_note = path_note or []
            self.sanitizer_note = sanitizer_note or []
        #先不要变量交换记录和上下文信息
        
        def _check_sanitization(self):
            '''
            检查净化是否充分
            '''
            pass

        def _is_sanitizer_source_and_sink(self):
            '''
            检查净化点位置
            '''
            pass

        def _check_sanitization_type(self):
            '''
            净化的漏洞类型
            '''
            pass

        def _classify_vulnerability(self):
            '''
            根据汇聚点漏洞分类
            '''
            pass

        def _calculate_confidence(self):
            '''
            计算路径置信度
            '''
            pass

        def _calculate_risk_score(self):
            '''
            计算风险评分
            '''
            pass

        def to_dict(self):
            '''
            用来序列化
            '''
            pass

        def get_path(self):
            '''
            路径绘制
            '''
            pass