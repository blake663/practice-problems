import re
import operator


class Machine(object):
    
    def __init__(self, cpu):
        self.cpu = cpu
    
    def execute(self, instr):
        instructions = re.match(
                r'^(?P<op>\w+?)(?P<push_a>a)?(?: (?P<src>\w*))?(?:, (?P<dest>\w*))?$',
                instr).groupdict()
        
        if instructions['push_a']:
            self.cpu.write_stack(self.cpu.read_reg('a'))
        
        op = instructions['op']
        src = instructions['src']
        src_val = self.cpu.read_reg(src) if src in 'abcd' else int(src)
        dest = instructions['dest']
        
        if op.startswith('pop'):
            if op == 'pop':
                self.cpu.pop_stack()
            elif op == 'popr':
                for reg in 'dcba':
                    self.cpu.write_reg(reg, self.cpu.pop_stack())
            elif op == 'poprr':
                for reg in 'abcd':
                    self.cpu.write_reg(reg, self.cpu.pop_stack())
            return   
        
        
        if op.startswith('push'):
            if op == 'push':
                self.cpu.write_stack(src_val)
            elif op == 'pushr':
                for reg in 'abcd':
                    self.cpu.write_stack(self.cpu.read_reg(reg))
            elif op == 'pushrr':
                for reg in 'dcba':
                    self.cpu.write_stack(self.cpu.read_reg(reg))
            return
        
        if op == 'mov':
            self.cpu.write_reg(dest, src_val)
            return
        
        
        result = self.cpu.pop_stack()
        for _ in range(src_val - 1):
            result = operator.__dict__[op](result, self.cpu.pop_stack())
        self.cpu.write_reg('a', result)
        return

