import * as React from "react";
import { useState } from "react";
import { Button, Field, Textarea, tokens, makeStyles } from "@fluentui/react-components";
import makeSocket from "../../wsconnect/wsconnect";
import { getRangeData } from "../office-document";
import { getCellRange } from "../office-document";

const useStyles = makeStyles({
  instructions: {
    fontWeight: tokens.fontWeightSemibold,
    marginTop: "20px",
    marginBottom: "10px",
  },
  textPromptAndInsertion: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
  },
  textAreaField: {
    marginLeft: "20px",
    marginTop: "30px",
    marginBottom: "20px",
    marginRight: "20px",
    maxWidth: "50%",
  },
});

const connection = makeSocket();
connection.on("message", function (msg) {
  console.log("Received message: ", msg);
});
console.log(connection);

const TextInsertion: React.FC = () => {
  const [inputs, setInputs] = useState({
    inputRange: "",
    outputRange: "",
    description: "",
  });

  const handleTextChange = async (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
  };
  const handleRetrieveRange = async (event) => {
    const { name } = event.target;
    var range = await getCellRange();
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: range,
    }));
  };

  const handleSubmit = async () => {
    var msg = {
      inputRange: inputs.inputRange,
      outputRange: inputs.outputRange,
      description: inputs.description,
      inputData: await getRangeData(inputs.inputRange),
      outputData: await getRangeData(inputs.outputRange),
    };
    connection.emit("message", msg);
    console.log("submitted!", msg);
  };

  const styles = useStyles();

  return (
    <div className={styles.textPromptAndInsertion}>
      <Field className={styles.textAreaField} size="large" label="Range of input data.">
        <Textarea size="large" name="inputRange" value={inputs.inputRange} onChange={handleTextChange} />
        <Button appearance="primary" name="inputRange" disabled={false} size="large" onClick={handleRetrieveRange}>
          Use selected cells
        </Button>
      </Field>
      <Field className={styles.textAreaField} size="large" label="Range of output data.">
        <Textarea size="large" name="outputRange" value={inputs.outputRange} onChange={handleTextChange} />
        <Button appearance="primary" name="outputRange" disabled={false} size="large" onClick={handleRetrieveRange}>
          Use selected cells
        </Button>
      </Field>
      <Field className={styles.textAreaField} size="large" label="Description.">
        <Textarea size="large" name="description" value={inputs.description} onChange={handleTextChange} />
      </Field>
      <Field className={styles.instructions}>
        Click the button to insert text.
        <Button appearance="primary" name="submit" disabled={false} size="large" onClick={handleSubmit}>
          Submit
        </Button>
      </Field>
    </div>
  );
};

export default TextInsertion;
