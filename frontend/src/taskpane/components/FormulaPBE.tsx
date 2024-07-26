import * as React from "react";
import { useState } from "react";
import {
  Field,
  Textarea,
  tokens,
  makeStyles,
  Label,
  ProgressBar,
  Dialog,
  DialogTrigger,
  DialogSurface,
  DialogTitle,
  DialogBody,
  DialogActions,
  DialogContent,
  Button,
  useRestoreFocusTarget,
  MessageBar,
  MessageBarTitle,
  MessageBarBody,
  MessageBarIntent,
  Link,
  Card,
  CardFooter,
  CardHeader,
  CardPreview,
  Body1,
  Caption1,
  BreadcrumbItem,
  Breadcrumb,
  BreadcrumbDivider,
  BreadcrumbButton,
  CounterBadge,
} from "@fluentui/react-components";
import {
  CalendarMonthFilled,
  CalendarMonthRegular,
  bundleIcon,
  BookToolboxRegular,
  RibbonStarFilled,
  LightbulbCheckmarkRegular,
  QuestionCircleRegular,
} from "@fluentui/react-icons";
import makeSocket from "../../wsconnect/wsconnect";
import { getRangeData, promptForAddressRange, recvRangeCandidate } from "../office-document";
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
    width: "100%",
    alignItems: "center",
  },
  textAreaField: {
    marginTop: "10px",
    marginBottom: "10px",
    maxWidth: "50%",
  },
  cardStyle: {
    marginTop: "10px",
    marginBottom: "10px",
    width: "90%",
  },
  topLabel: {
    backgroundColor: "#f0ebe5",
    alignItems: "center",
    textAlign: "center",
    justifyContent: "center",
    height: "30px",
    width: "100%",
    marginBottom: "10px",
    boxShadow: "0 4px 4px 0 rgba(0, 0, 0, 0.2), 0 6px 10px 0 rgba(0, 0, 0, 0.19)",
  },
  finst: {
    width: "100%",
  },
});

const FormulaPBE: React.FC = () => {
  const connection = makeSocket();
  connection.on("message", function (msg) {
    recvRangeCandidate(msg);
    setProgressOpen(false);
    if (msg["status"] == "ok") {
      feedbackDialogRestore();
      setFeedbackOpen(true);
    } else {
      setFailedOpen(true);
    }
  });
  console.log(connection);

  const [inputs, setInputs] = useState({
    inputRange: "(No Selected)",
    outputRange: "(No Selected)",
    description: "",
    feedbackMsg: "",
    submitIsDisabled: false,
    loadingIsHidden: true,
    furtherInst: false,
  });

  const [progressOpen, setProgressOpen] = React.useState(false);
  const [feedbackOpen, setFeedbackOpen] = React.useState(false);
  const [failedOpen, setFailedOpen] = React.useState(false);
  const feedbackDialogRestore = () => {
    setInputs((prevInputs) => ({
      ...prevInputs,
      furtherInst: false,
    }));
  };
  const restoreFocusTargetAttribute = useRestoreFocusTarget();

  const handleTextChange = async (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: value,
    }));
  };
  const handleRetrieveRange = async (event) => {
    const { name } = event.target;
    // var range = await getCellRange();
    var range = await promptForAddressRange();
    setInputs((prevInputs) => ({
      ...prevInputs,
      [name]: range,
    }));
  };

  const handleSubmit = async () => {
    var msg = {
      type: "formula_pbe",
      inputRange: inputs.inputRange,
      outputRange: inputs.outputRange,
      description: inputs.description,
      feedbackMsg: inputs.feedbackMsg,
      inputData: await getRangeData(inputs.inputRange),
      outputData: await getRangeData(inputs.outputRange),
    };
    connection.emit("message", msg);
    setProgressOpen(true);

    console.log("submitted!", msg);
  };

  const handleFeedback = async () => {
    var msg = {
      type: "feedback",
      feedbackMsg: inputs.feedbackMsg,
    };
    connection.emit("message", msg);
    setProgressOpen(true);
    console.log("submitted!", msg);
  };

  const styles = useStyles();

  return (
    <div className={styles.textPromptAndInsertion}>
      <Breadcrumb aria-label="Breadcrumb default example">
        <BreadcrumbItem>
          <BreadcrumbButton icon={<BookToolboxRegular />}>Formula PBE</BreadcrumbButton>
        </BreadcrumbItem>
      </Breadcrumb>
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Getting started with Formula Programming by Example (PBE)</b>
            </Body1>
          }
          description={
            <Caption1>
              PowerSheet PBE allows you to get the formula by providing the expected result of it. Get started with PBE
              by the following steps.
            </Caption1>
          }
        />
        <Label>
          <CounterBadge size="small" count={1} appearance="filled"></CounterBadge>
          &nbsp;Write down the <b>expected result</b> of the formula in the target cell.
        </Label>
        <Label>
          <CounterBadge size="small" count={2} appearance="filled"></CounterBadge>
          &nbsp;Determine the cell that <b>should be referenced</b> in the formula.
        </Label>
        <Label>
          <CounterBadge size="small" count={3} appearance="filled"></CounterBadge>
          &nbsp;Write down <b>additional descriptions</b> if the formula is complex. (Optional)
        </Label>
      </Card>
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Referencing Data</b>
            </Body1>
          }
          description={<Caption1>Select the data that should be referenced by the formula.</Caption1>}
        />
        <Label weight="semibold">{inputs.inputRange}</Label>
        <Button name="inputRange" disabled={false} size="medium" onClick={handleRetrieveRange}>
          Select Cells
        </Button>
      </Card>

      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Formula Example</b>
            </Body1>
          }
          description={<Caption1>Select the example of formula results.</Caption1>}
        />
        <Label weight="semibold">{inputs.outputRange}</Label>
        <Button name="outputRange" disabled={false} size="medium" onClick={handleRetrieveRange}>
          Select Cells
        </Button>
      </Card>

      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Description (Optional)</b>
            </Body1>
          }
          description={
            <Caption1>
              Write additional information that you want Ryzen AI to know, for better generation results.
            </Caption1>
          }
        />
        <Textarea size="large" name="description" value={inputs.description} onChange={handleTextChange} />
      </Card>

      <Field className={styles.cardStyle}>
        <Button
          appearance="primary"
          name="submit"
          disabled={inputs.submitIsDisabled}
          size="large"
          onClick={handleSubmit}
        >
          Generate Formula
        </Button>
      </Field>
      <Label>
        <RibbonStarFilled />
        Powered by AMD <b>Ryzen AI</b>
      </Label>

      {/* <Field className={styles.textAreaField} size="large" label="Feedback message.">
        <Textarea size="large" name="feedbackMsg" value={inputs.feedbackMsg} onChange={handleTextChange} />
        <Button appearance="primary" name="feedbackSubmit" disabled={false} size="large" onClick={handleFeedback}>
          Send feedback
        </Button>
      </Field> */}

      <Dialog
        // this controls the dialog open state
        open={progressOpen}
        onOpenChange={(_, data) => {
          // it is the users responsibility to react accordingly to the open state change
          setProgressOpen(data.open);
        }}
      >
        <DialogSurface>
          <DialogBody>
            <DialogContent>
              <Field validationMessage="Ryzen AI is thinking..." validationState="none">
                <ProgressBar />
              </Field>
            </DialogContent>
          </DialogBody>
        </DialogSurface>
      </Dialog>

      <Dialog
        // this controls the dialog open state
        open={feedbackOpen}
        onOpenChange={(_, data) => {
          // it is the users responsibility to react accordingly to the open state change
          setFeedbackOpen(data.open);
        }}
      >
        <DialogSurface>
          <DialogBody>
            <DialogTitle>
              <LightbulbCheckmarkRegular />
              &nbsp;Your cell content is replaced with generated formula!
            </DialogTitle>
            <DialogContent>
              <Label style={{ display: inputs.furtherInst ? "none" : "block" }}>
                Check your worksheet to see whether it meets your goal.
              </Label>
              <Field
                label="Input further instruction"
                className={styles.finst}
                style={{ display: inputs.furtherInst ? "block" : "none" }}
              >
                <Textarea
                  name="feedbackMsg"
                  value={inputs.feedbackMsg}
                  onChange={handleTextChange}
                  className={styles.finst}
                />
              </Field>
            </DialogContent>

            <DialogActions>
              <Button
                appearance="secondary"
                onClick={() => {
                  setInputs((prevInputs) => ({
                    ...prevInputs,
                    furtherInst: true,
                  }));
                }}
                style={{ display: inputs.furtherInst ? "none" : "block" }}
              >
                Further Instruction
              </Button>
              <Button
                appearance="primary"
                onClick={() => {
                  if (inputs.furtherInst) {
                    handleFeedback();
                  }
                  setFeedbackOpen(false);
                }}
              >
                {inputs.furtherInst ? "Submit" : "Accept"}
              </Button>
            </DialogActions>
          </DialogBody>
        </DialogSurface>
      </Dialog>
      <Dialog
        // this controls the dialog open state
        open={failedOpen}
        onOpenChange={(_, data) => {
          // it is the users responsibility to react accordingly to the open state change
          setFailedOpen(data.open);
        }}
      >
        <DialogSurface>
          <DialogBody>
            <DialogTitle>
              <QuestionCircleRegular />
              &nbsp;Oops... Ryzen AI gets a bit confused here.
            </DialogTitle>
            <DialogContent>
              <Label>
                Narrow the scope of input or output and provide a more precise description to help the model understand.
              </Label>
            </DialogContent>

            <DialogActions>
              <Button
                appearance="primary"
                onClick={() => {
                  setFailedOpen(false);
                }}
              >
                Close
              </Button>
            </DialogActions>
          </DialogBody>
        </DialogSurface>
      </Dialog>
    </div>
  );
};

export default FormulaPBE;
