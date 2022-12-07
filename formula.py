# strcar ( string ) : Calculates the string with the formula attached.
def strcar(string):
    stack = []
    now_num = -1

    try:
        # Check the entire string. ( using ch )
        for ch in string:  
            if ch in ['+', '-', '*', '/', '%', '(', ')']: # Operator
                if now_num != -1: # Append the number in stack
                    stack.append(now_num)
                    now_num = -1

                if ch == ')': # Calculate an expression in parentheses
                    now_result = stack[-1]
                    stack.pop()

                    while True:
                        if len(stack) == 0: return "Error"

                        if stack[-1] == '(':
                            stack.pop()
                            stack.append(now_result)
                            break

                        else:
                            if stack[-1] == '+': now_result = stack[-2] + now_result
                            elif stack[-1] == '-': now_result = stack[-2] - now_result
                            elif stack[-1] == '*': now_result = stack[-2] * now_result
                            elif stack[-1] == '/': now_result = int(stack[-2] // now_result)
                            elif stack[-1] == '%': now_result = stack[-2] % now_result

                            for _ in range(2): stack.pop() 
                                           
                else: # +, -, *, /, %, (
                    stack.append(ch)
            
            else: # Stack number
                if now_num == -1: now_num = 0
                now_num = now_num * 10 + int(ch)

        # The last number
        if now_num != -1: 
            stack.append(now_num)
        
        # Calculate Preferred Operators First
        idx = 0
        while idx < len(stack):
            if stack[idx] in ['*', '/', '%']:
                if stack[idx] == '*':
                    stack[idx - 1] = stack[idx - 1] * stack[idx + 1]
                elif stack[idx] == '/':
                    stack[idx - 1] = int(stack[idx - 1] // stack[idx + 1])
                elif stack[idx] == '%':
                    stack[idx - 1] = stack[idx - 1] % stack[idx + 1]

                for _ in range(2): del stack[idx]
            else: idx += 1
        
        # Calculate the remaining operations
        while len(stack) != 1:
            if stack[1] == '+': stack[0] = stack[0] + stack[2]
            elif stack[1] == '-': stack[0] = stack[0] - stack[2]
            else: return "Error"

            for _ in range(2): del stack[1]
        
        if len(stack) == 1 and (stack[0] not in ['+', '-', '*', '/', '%', '(']): return stack[0]
        else: return "Error"
        
    except ZeroDivisionError: return "Zero Division"
    except: return "Error"
