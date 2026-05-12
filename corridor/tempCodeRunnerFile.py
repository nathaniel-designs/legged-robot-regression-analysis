    # Shift to start at 0
    t_ref_elapsed = t_ref - t_ref[0]
    
    interpolation_func = interp1d(t_init, footforces, kind='linear', fill_value='extrapolate')
    f_aligned = interpolation_func(t_ref_elapsed)