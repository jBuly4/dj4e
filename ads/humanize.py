def naturalsize(count):
    float_count = float(count)
    k = 1024
    m = k * k
    g = m * k
    if float_count < k:
        return str(count) + 'B'
    if k <= float_count < m:
        return str(int(float_count / (k / 10.0)) / 10.0) + 'KB'
    if m <= float_count < g:
        return str(int(float_count / (m / 10.0)) / 10.0) + 'MB'
    return str(int(float_count / (g / 10.0)) / 10.0) + 'GB'
