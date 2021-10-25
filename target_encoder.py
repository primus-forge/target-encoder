def df__cols__target_encoder(df, cols, drop_invariant, handle_missing, handle_unknown, min_samples_leaf, smoothing,
                             output_cols=None):
    def _target_encoder(series, drop_invariant, handle_missing, handle_unknown, min_samples_leaf, smoothing):

        from category_encoders import TargetEncoder
        imputer = TargetEncoder(drop_invariant=drop_invariant, handle_missing=handle_missing,
                                handle_unknown=handle_unknown, min_samples_leaf=min_samples_leaf, smoothing=smoothing)
        return imputer.fit_transform(series.values.reshape(-1, 1))

    from optimus.helpers.columns import parse_columns, get_output_cols, prepare_columns_arguments

    cols = parse_columns(df, cols)

    n_neighbors, weights, metric = prepare_columns_arguments(cols, drop_invariant, handle_missing, handle_unknown,
                                                             min_samples_leaf, smoothing)
    output_cols = get_output_cols(cols, output_cols)

    for col_name, output_col, _n_neighbors, _weights, _metric in zip(cols, output_cols, n_neighbors, weights, metric):
        df = df.cols.to_float(col_name)
        df = df.cols.apply(col_name, _target_encoder, output_cols=output_col, args=(_n_neighbors, _weights, _metric),
                           mode="vectorized")

    return df
