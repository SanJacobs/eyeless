def progress(length, progress, completion_point):
    
    completion = float(progress)/completion_point
    
    fill = int(completion*length)
    clear = length-fill
    
    return str("[" + "#"*fill + "·"*clear + "]")


if __name__ == "__main__":
    print(progress(10, 4, 8))
