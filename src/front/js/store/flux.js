import { element } from "prop-types";

const getState = ({ getStore, getActions, setStore }) => {
  return {
    store: {
      token: "",
      validacion: false,
      eventos: [],
      eventosFilter: [],
    },
    actions: {
      filterEvent: (event) => {
        const eventos = getStore().eventos;
        console.log(event, "properties");
        const paymentResults =
          event.payment == null
            ? eventos
            : event.payment == true
            ? eventos.filter((element) => element.payment > 0)
            : eventos.filter((element) => element.payment == 0);
        const spaceResult =
          event.space == null
            ? paymentResults
            : event.space == true
            ? paymentResults.filter((element) => element.space == true)
            : paymentResults.filter((element) => element.space == false);
        const durationResults = spaceResult.filter(
          (element) => element.duration >= event.duration
        );
        const ageminResults = durationResults.filter(
          (element) => element.agemin >= event.agemin
        );
        const agemaxResults = ageminResults.filter(
          (element) => element.agemax <= event.agemax
        );

        const dateResults =
          event.date !== ""
            ? agemaxResults.filter((element) => element.date == event.date)
            : agemaxResults;

        setStore({ eventosFilter: dateResults });
      },
      joinEvent: (event) => {
        const store = getStore();
        fetch(process.env.BACKEND_URL + "/api/joinevent", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            Authorization: "Bearer " + store.token,
          },
          body: JSON.stringify({
            id: event,
          }),
        }).then((resp) => {
          if (resp.ok) {
            alert("usuario registrado");
          }
        });
      },

      logout: () => {
        setStore({ token: "" });
        sessionStorage.removeItem("token");
        setStore({ validacion: false });
      },

      login: (email, password) => {
        fetch(process.env.BACKEND_URL + "/api/token", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        })
          .then((respuestadelback) => {
            if (respuestadelback.status == 200) {
              return respuestadelback.json();
            } else if (respuestadelback.status == 401) {
              console.log("El email o password es incorrecto o no existe, 401");
            } else if (respuestadelback.status == 402) {
              console.log("El email o password es incorrecto o no existe, 402");
            }
          })
          .then((respuestajson) => {
            sessionStorage.setItem("token", respuestajson.access_token);
            setStore({ token: respuestajson.access_token });
            setStore({ validacion: true });
          });
      },

      //FUNCION reloadToken PARA QUE NO SE PIERDA EL TOKEN DEL STORAGE
      reloadToken: () => {
        let datotoken = sessionStorage.getItem("token");
        if (datotoken !== "" && datotoken !== null && datotoken !== undefined) {
          setStore({ token: datotoken });
          setStore({ validacion: true });
        }
      },

      // Use getActions to call a function within a fuction
      exampleFunction: () => {
        getActions().changeColor(0, "green");
      },
      getEventos: () => {
        fetch(process.env.BACKEND_URL + "/api/eventos", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        })
          .then((resp) => {
            if (resp.status == 200) {
              return resp.json();
            } else {
              console.log(resp.json());
            }
          })
          .then((data) => {
            setStore({ eventos: data });
            setStore({ eventosFilter: data });
          });
      },

      getMessage: async () => {
        try {
          // fetching data from the backend
          const resp = await fetch(process.env.BACKEND_URL + "/api/hello");
          const data = await resp.json();
          setStore({ message: data.message });
          // don't forget to return something, that is how the async resolves
          return data;
        } catch (error) {
          console.log("Error loading message from backend", error);
        }
      },
      changeColor: (index, color) => {
        //get the store
        const store = getStore();

        //we have to loop the entire demo array to look for the respective index
        //and change its color
        const demo = store.demo.map((elm, i) => {
          if (i === index) elm.background = color;
          return elm;
        });

        //reset the global store
        setStore({ demo: demo });
      },
    },
  };
};

export default getState;
