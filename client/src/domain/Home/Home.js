import React, { useMemo, useState } from "react";
import {
  Button,
  Grid,
  List,
  ListItem,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { useForm } from "react-hook-form";
import { createBeer } from "../../common/services/formService";
import { Loading, Select } from "../../common/components";
import { ALL_TYPES } from "../../common/utils/constants";
import BeerType from "./BeerType";

const TRAD = {
  intensity: "Intensidad",
  color: "Oscuridad",
  bitterness: "Amargor",
  hop: "Lúpulo",
  fermentation: "Fermentación",
  yeast: "Levadura",
  baja: "Baja",
  media: "Media",
  alta: "Alta",
  palido: "Pálido",
  ambar: "Ámbar",
  oscuro: "Oscuro",
  bajo: "Bajo",
  medio: "Medio",
  alto: "Alto",
  "viejo mundo": "Viejo mundo",
  "nuevo mundo": "Nuevo mundo",
  lager: "Lager",
  ale: "Ale",
}

export default function Home() {
  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    resetField,
    getValues,
  } = useForm();
  const [candidateBeers, setCandidateBeers] = useState([]);
  const [used, setUsed] = useState(false);
  const [step, setStep] = useState("intensity");
  const [lastStep, setLastStep] = useState(false);
  const [stepsGiven, setStepsGiven] = useState([]);
  const [candBeersGiven, setCandBeersGiven] = useState([]);
  const [loading, setLoading] = useState(false);

  const intensityStep = useMemo(
    () => (
      <Select register={register} errors={errors} {...ALL_TYPES.intensity} />
    ),
    []
  );
  const colorStep = useMemo(
    () => <Select register={register} errors={errors} {...ALL_TYPES.color} />,
    []
  );
  const bitternessStep = useMemo(
    () => (
      <Select register={register} errors={errors} {...ALL_TYPES.bitterness} />
    ),
    []
  );
  const hopStep = useMemo(
    () => <Select register={register} errors={errors} {...ALL_TYPES.hop} />,
    []
  );
  const fermentationStep = useMemo(
    () => (
      <Select register={register} errors={errors} {...ALL_TYPES.fermentation} />
    ),
    []
  );
  const yeastStep = useMemo(
    () => <Select register={register} errors={errors} {...ALL_TYPES.yeast} />,
    []
  );

  const theme = createTheme({
    palette: {
      primary: {
        main: "#000000",
      },
      secondary: {
        main: "#ffffff",
      },
    },
  });

  const steps = {
    intensity: intensityStep,
    color: colorStep,
    bitterness: bitternessStep,
    hop: hopStep,
    fermentation: fermentationStep,
    yeast: yeastStep,
  };

  const setBackStep = async () => {
    setLoading(true);
    console.log(stepsGiven);
    console.log(step);
    if (stepsGiven.length) {
      if (stepsGiven.length === 1) setUsed(false);

      resetField(step);
      setStep(stepsGiven.at(-1));
      setCandidateBeers(candBeersGiven.at(-1));
      setStepsGiven((sg) => sg.slice(0, -1));
      setCandBeersGiven((cbg) => cbg.slice(0, -1));
      setLastStep(false);
    }

    setLoading(false);
  };

  const onSubmit = async (data) => {
    if (lastStep) return;
    setLoading(true);

    try {
      const posBeers = await createBeer(data);
      setCandidateBeers(posBeers.candidateBeers);
      setStepsGiven((sg) => sg.concat(step));
      setCandBeersGiven((cbg) => cbg.concat([candidateBeers]));
      setStep(posBeers.nextQuestion);
      setUsed(true);

      if (posBeers.candidateBeers.length <= 1) setLastStep(true);
    } catch (error) {
      console.log(error);
      console.log(errors);
    }
    setLoading(false);
  };

  const resetAll = () => {
    reset();
    setCandidateBeers([]);
    setUsed(false);
    setStep("intensity");
    setLastStep(false);
    setStepsGiven([]);
    setCandBeersGiven([]);
  };

  const beerForm = (
    <Stack width="80%" height="100%" justifyContent="center" margin="auto">
      <form onSubmit={handleSubmit(onSubmit)}>
        {loading ? (
          <Loading />
        ) : (
          <ThemeProvider theme={theme}>
            <Stack spacing={10} justifyContent="center" alignItems="center">
              {steps[step]}
              <Stack
                flexDirection="row"
                justifyContent="space-around"
                width="100%"
              >
                {stepsGiven.length ? (
                  <div>
                    <Button onClick={setBackStep} variant="contained">
                      Volver
                    </Button>
                  </div>
                ) : null}
                <div>
                  <Button type="submit" variant="contained">
                    {lastStep ? "Enviar" : "Continuar"}
                  </Button>
                </div>
              </Stack>
            </Stack>
          </ThemeProvider>
        )}
      </form>
    </Stack>
  );

  console.log(getValues())

  const resultForm = (
    <Stack width="80%" height="100%" justifyContent="center" margin="auto">
      {loading ? (
        <Loading />
      ) : (
        <ThemeProvider theme={theme}>
          <Stack spacing={10} justifyContent="center" alignItems="center">
            <Typography variant="h3">Resultado encontrado</Typography>
            <Stack spacing={1}>
            <Typography variant="h6">Porque elegiste...</Typography>
            {
              Object.entries(getValues()).map(v => 
                v[1] && <Typography>- {TRAD[v[0]]}: {TRAD[v[1]]}</Typography>
              )
            }
            </Stack>
            <Stack
              flexDirection="row"
              justifyContent="space-around"
              width="100%"
            >
              <div>
                <Button onClick={setBackStep} variant="contained">
                  Volver
                </Button>
              </div>
              <div>
                <Button onClick={resetAll} variant="contained">
                  Reiniciar
                </Button>
              </div>
            </Stack>
          </Stack>
        </ThemeProvider>
      )}
    </Stack>
  );

  const candidateBeersToShow = (
    <Stack width="80%" height="100%" justifyContent="center" margin="auto">
      {candidateBeers.length === 1 && <BeerType name={candidateBeers[0]} />}
      {!used && (
        <div>
          <Typography>Para comenzar, responda la primera pregunta</Typography>
        </div>
      )}
      {candidateBeers.length === 0 && used && (
        <div>
          <Typography color={"red"}>
            No pudimos encontrar una cerveza que cumpla con las especificaciones
            provistas
          </Typography>
        </div>
      )}
      {candidateBeers.length > 1 && (
        <div>
          <Typography>
            Estamos analizando las especificaciones provistas. Las posibles
            cervezas hasta el momento son:
          </Typography>
          <List>
            {candidateBeers.map((b) => (
              <ListItem dense key={`LI${b}`}>
                <Typography>{`- ${b}`}</Typography>
              </ListItem>
            ))}
          </List>
          <Typography>Porque elegiste...</Typography>
            <List>
              {Object.entries(getValues()).map(v =>
                v[0] !== step && v[1] &&
                <ListItem dense key={`LI${v[0]}`}>
                  <Typography>- {TRAD[v[0]]}: {TRAD[v[1]]}</Typography>
                </ListItem>
              )}
            </List>
        </div>
      )}
    </Stack>
  );

  return (
    <Grid container spacing={2} height="100%">
      <Grid item xs={8}>
        {lastStep ? resultForm : beerForm}
      </Grid>
      <Grid item xs={4}>
        {candidateBeersToShow}
      </Grid>
    </Grid>
  );
}
