import random

class CFG:
    def __init__(self, non_terminals, terminals, productions, start_symbol):
        # non_terminals: A set of non-terminal symbols (strings)
        # terminals: A set of terminal symbols (strings)
        # productions: A dictionary where keys are non-terminals and values are lists of
        #              production rules. Each rule is a list of symbols (terminals or non-terminals)
        #              Epsilon is represented by an empty list []
        #              Example: {'S': [['a', 'S', 'b'], []]}
        # start_symbol: The start symbol (string)
        self.non_terminals = set(non_terminals)
        self.terminals = set(terminals)
        self.productions = productions
        self.start_symbol = start_symbol
        self._derivation_path_result = []


    def generate_strings(self, num_strings, max_length, max_recursion_depth=15):
        # generates a specified number of unique strings from the CFG
        # limits string length and recursion depth for generation
        generated_strings = set()
        attempts = 0
        max_attempts = num_strings * 20 + 100 

        while len(generated_strings) < num_strings and attempts < max_attempts:
            string = self._generate_recursive_string([self.start_symbol], max_length, 0, max_recursion_depth)
            if string is not None:
                generated_strings.add(string)
            attempts += 1
        return list(generated_strings)

    def _generate_recursive_string(self, current_form, max_len, depth, max_depth):
        # current_form: A list of symbols representing the current sentential form
        # max_len: Maximum length of the final terminal string
        # depth: Current recursion depth
        # max_depth: Maximum allowed recursion depth
        if depth > max_depth:
            # if too deep, attempt to resolve to terminals only if all NTs are nullable
            term_form_parts = []
            for sym in current_form:
                if sym in self.terminals:
                    term_form_parts.append(sym)
                elif sym in self.non_terminals: # this case means we are at an S symbol
                    pass 
                    
            s = "".join(term_form_parts)
            return s if len(s) <= max_len else None

        # check if current terminals-only part of the form already exceeds max_len
        terminals_so_far_len = sum(len(s) for s in current_form if s in self.terminals)
        if terminals_so_far_len > max_len:
            return None

        # check for non-terminals in the current form
        nt_idx = -1
        for i, symbol in enumerate(current_form):
            if symbol in self.non_terminals:
                nt_idx = i
                break

        if nt_idx == -1:
            final_string = "".join(current_form)
            return final_string if len(final_string) <= max_len else None

        # we have a non-terminal to expand
        nt_to_expand = current_form[nt_idx]
        prefix = current_form[:nt_idx]
        suffix = current_form[nt_idx+1:]

        # get productions for this non-terminal and shuffle for randomness
        possible_rules = list(self.productions[nt_to_expand])
        random.shuffle(possible_rules)

        for rule_rhs in possible_rules:
            new_form = prefix + rule_rhs + suffix
            
            result_string = self._generate_recursive_string(new_form, max_len, depth + 1, max_depth)
            if result_string is not None:
                return result_string        
        return None

    def get_derivation_and_membership(self, target_string, max_deriv_steps=30):
        # max_deriv_steps: max derivation steps (wrong grammer or too deep recursion)
        # returns; 1/0 (if in cfg), and derivation path

        target_list = list(target_string)
        self._derivation_path_result = []
        is_member = self._parse_recursive(
            current_form=[self.start_symbol],
            target_list=target_list,
            current_derivation_trace=[self.start_symbol],
            max_deriv_steps=max_deriv_steps
        )
        
        if is_member:
            return True, self._derivation_path_result
        else:
            return False, []

    def _parse_recursive(self, current_form, target_list, current_derivation_trace, max_deriv_steps):
        # current_form: list of symbols in the current sentential form
        # target_list: list of characters in the target string
        # current_derivation_trace: list of strings representing the derivation steps so far
        
        if self._derivation_path_result and self._derivation_path_result == current_derivation_trace:
             return True 

        if len(current_derivation_trace) > max_deriv_steps:
            return False

        form_terminals_prefix = []
        first_nt_index_in_form = -1 
        for i, sym in enumerate(current_form):
            if sym in self.terminals:
                form_terminals_prefix.append(sym)
            else:
                first_nt_index_in_form = i
                break
        
        if len(form_terminals_prefix) > len(target_list):
            return False
        
        if form_terminals_prefix != target_list[:len(form_terminals_prefix)]:
            return False
        
        # all symbols in current_form are terminals
        if first_nt_index_in_form == -1:
            if current_form == target_list:
                if not self._derivation_path_result or len(current_derivation_trace) < len(self._derivation_path_result) :
                    self._derivation_path_result = list(current_derivation_trace)
                return True
            else:
                return False

        # extend the leftmost non-terminal
        nt_to_expand = current_form[first_nt_index_in_form]
        prefix_before_nt = current_form[:first_nt_index_in_form]
        suffix_after_nt = current_form[first_nt_index_in_form+1:]

        for rule_rhs in self.productions[nt_to_expand]:
            new_form = prefix_before_nt + rule_rhs + suffix_after_nt
            new_form_str = "".join(new_form) if new_form else 'ε'
            current_derivation_trace.append(new_form_str)
            if self._parse_recursive(new_form, target_list, current_derivation_trace, max_deriv_steps):
                return True
            current_derivation_trace.pop()
        return False 
    
cfg_S_aSb_eps = CFG(
    non_terminals={'S'},
    terminals={'a', 'b'},
    productions={
        'S': [['a', 'S', 'b'], []]
    },
    start_symbol='S'
)

def recognize_anbncn(s):
    if not s: 
        return False
    length = len(s)

    idx = 0
    while idx < length and s[idx] == 'a':
        idx += 1
    num_a = idx
    if num_a == 0:
        return False

    start_b = idx
    while idx < length and s[idx] == 'b':
        idx += 1
    num_b = idx - start_b
    if num_b != num_a: 
        return False
    
    start_c = idx
    while idx < length and s[idx] == 'c':
        idx += 1
    num_c = idx - start_c
    if num_c != num_a:
        return False
        
    if idx != length:
        return False
    return True 

def main():
    print("--- Task 1: CFG Definition (S -> aSb | ε) ---")
    print(f"Non-terminals: {cfg_S_aSb_eps.non_terminals}")
    print(f"Terminals: {cfg_S_aSb_eps.terminals}")
    print(f"Start Symbol: {cfg_S_aSb_eps.start_symbol}")
    print("Productions:")
    for nt, rules in cfg_S_aSb_eps.productions.items():
        for r in rules:
            print(f"  {nt} -> {''.join(r) if r else 'ε'}")
    print("-" * 40)

    print("\n--- Task 2: String Generator (for S -> aSb | ε) ---")
    generated_s_ab = cfg_S_aSb_eps.generate_strings(num_strings=10, max_length=10, max_recursion_depth=7)
    print(f"Generated up to 10 strings (max length 10): {sorted(generated_s_ab, key=len)}")
    print("-" * 40)

    print("\n--- Task 3 & 4: Derivation and Membership (for S -> aSb | ε) ---")
    test_strings_ab = ["", "ab", "aabb", "aaabbb", "aab", "aabbc", "abab", "aaaaabbbbb"]
    test_strings_ab.append("aaaaaabbbbbb") # length 12
    
    for ts in test_strings_ab:
        print(f"\nTesting string: '{ts}' (length {len(ts)})")
        max_steps = len(ts) + 5 
        is_member, derivation = cfg_S_aSb_eps.get_derivation_and_membership(ts, max_deriv_steps=max_steps)
        print(f"  Belongs to L(G) (S -> aSb | ε): {is_member}")
        if is_member:
            print(f"  Derivation: {' -> '.join(derivation)}")
        if len(ts) > 12 and not is_member:
             print(f"  (Note: String length > 12. Official requirement for tester is up to length 12.)")
    print("-" * 40)

    print("\n--- Task 5: Bonus - Recognizer for L = {a^n b^n c^n | n >= 1} ---")
    print("This language L = {a^n b^n c^n | n >= 1} is NOT context-free.")
    print("This can be proven using the Pumping Lemma for Context-Free Languages.")
    print("A CFG essentially has one 'stack' or counter, but this language requires two linked counts")
    print("(the number of 'b's must match 'a's, AND 'c's must match 'a's/'b's).")
    print("The following is a direct recognizer, not based on a (non-existent) CFG for this language.")
    
    test_strings_anbncn = ["abc", "aabbcc", "aaabbbccc", 
                           "", "ab", "aabbc", "aaabbbcccddd", 
                           "aabbbccc", "aaabcc", "aabbccbbaa"]
    for ts in test_strings_anbncn:
        is_member_anbncn = recognize_anbncn(ts)
        print(f"String '{ts}': Belongs to L = {{a^n b^n c^n | n >= 1}}: {is_member_anbncn}")
    print("-" * 40)

if __name__ == "__main__":
    main()