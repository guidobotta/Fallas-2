import React from "react";
import { FormControl, InputLabel, Select as MUISelect, MenuItem, Stack, Typography } from "@mui/material";

export default function Select({
  register,
  label,
  idLabel,
  values,
  errors,
  description,
}) {
  return (
    <Stack width="100%" spacing={3}>
      <Typography variant="h3" textAlign="center" fontWeight={600}>{label}</Typography>
      <Typography variant="h5">{description}</Typography>
      <FormControl fullWidth>
        <InputLabel>{label}</InputLabel>
        <MUISelect
          fullWidth
          label={label}
          labelId={idLabel}
          {
            ...register(idLabel, { required: true })
          }
        >
          {values.map(value => <MenuItem key={`SL-${value.value}`} value={value.value}>{value.name}</MenuItem>)}
        </MUISelect>
        {errors[idLabel] && <Typography marginTop={1} color="red">Debes completar este campo</Typography>}
      </FormControl>
    </Stack>
  )
}
