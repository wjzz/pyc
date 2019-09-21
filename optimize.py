def optimize(asm):
    start_label = "_start:"
    lines = asm.split(start_label,maxsplit=1)
    assert(len(lines) == 2)
    preamble = lines[0] + start_label + "\n"
    print("===", preamble, "===")
    rest = [ s.strip() for s in lines[1].splitlines() 
      if s != ""]
    print(rest)

    optimized_rest = apply_reductions_top(rest)

    optimized_asm = preamble + optimized_rest
    return asm

def apply_reductions_top(commands):
    total = len(commands)
    changed = True
    reducers = [red_push_pop, red_mov_trans, red_mov_r_r]
    while changed:
        changed = False
        for i in range(total):
            if changed:
                break
            for fun in reducers:
                opt = fun(commands[i:])
                if opt is not None:
                    commands[i:] = opt
                    changed = True
                    break
    print(commands)
    return "\n".join(commands)

def red_push_pop_star(commands):
    """
    Looks for patterns of the form
    push x1
    push x2
    ...
    push xn
    pop an
    ...
    pop a2
    pop a1
    and transforms them into
    mov an, xn
    ...
    mov a2, x2
    mov a1, x1
    """
    if len(commands) < 2:
        return None
    
    pushes = []
    ...

def red_push_pop(commands):
    if len(commands) < 2:
        return None
    try:
        first, second, *rest = commands
        tag1, args1 = first.split(" ", maxsplit=1)
        tag2, args2 = second.split(" ", maxsplit=1)
    except:
        return None

    if tag1 != "push" or tag2 != "pop":
        return None
    print(f"push; pop detected!")
    print(f"push to {args1}; pop to {args2}")
    cmd = f"mov {args2}, {args1}"
    print(f"==> {cmd}")
    print()
    return [cmd] + rest

def red_mov_r_r(commands):
    if len(commands) < 1:
        return None
    try:
        first, *rest = commands
        tag1, args = first.split(" ", maxsplit=1)
        arg1, arg2 = [s.strip() for s in args.split(",")]
    except:
        return None

    if tag1 != "mov" or arg1 != arg2:
        return None
    print(f"mov X, X detected!")
    print(f"mov from {arg1} to {arg2}")
    print(f"==> noop")
    print()
    return rest

def red_mov_trans(commands):
    if len(commands) < 2:
        return None
    try:
        first, second, *rest = commands
        tag1, args1 = first.split(" ", maxsplit=1)
        tag2, args2 = second.split(" ", maxsplit=1)
        arg1a, arg1b = [s.strip() for s in args1.split(",")]
        arg2a, arg2b = [s.strip() for s in args2.split(",")]
    except:
        return None

    if tag1 != "mov" or tag2 != "mov":
        return None
    if arg1a != arg2b:
        return None

    print(f"mov Y, X; mov X, Z detected")
    print(f"X = {arg1b}, Y = {arg1a}, Z = {arg2b}")
    #cmd = f"mov {args2}, {args1}"
    #print(f"==> {cmd}")
    print()
    return None
    return [cmd1, cmd2] + rest
