import * as React from "react";
import { useState } from "react";
import { DismissRegular } from "@fluentui/react-icons";
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
  MessageBar,
  MessageBarActions,
  MessageBarBody,
  MessageBarTitle,
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
import { getRangeData, getRangeFormula, promptForAddressRange, recvRangeCandidate } from "../office-document";
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
    whiteSpace: "pre-line",
  },
});

const CompChk: React.FC = () => {
  const connection = makeSocket();
  connection.on("message", function (msg) {
    // recvRangeCandidate(msg);
    setProgressOpen(false);
    setInfos(msg["info"]);
    if (msg["status"] == "ok") {
      // feedbackDialogRestore();
      // setFeedbackOpen(true);
      setInputs((prevInputs) => ({
        ...prevInputs,
        feedbackMsg: msg["reply"],
      }));
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

  const [infos, setInfos] = React.useState([]);

  const [progressOpen, setProgressOpen] = React.useState(false);
  const [feedbackOpen, setFeedbackOpen] = React.useState(false);
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
      type: "formula_chk",
      inputRange: inputs.inputRange,
      description: inputs.description,
      feedbackMsg: inputs.feedbackMsg,
      inputData: await getRangeFormula(inputs.inputRange),
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
          <BreadcrumbButton icon={<BookToolboxRegular />}>Compatibility Check</BreadcrumbButton>
        </BreadcrumbItem>
      </Breadcrumb>
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Cells Range</b>
            </Body1>
          }
          description={<Caption1>Select the formulas you want PowerSheet to perform compability check.</Caption1>}
        />
        <Label weight="semibold">{inputs.inputRange}</Label>
        <Button name="inputRange" disabled={false} size="medium" onClick={handleRetrieveRange}>
          Select Cells
        </Button>
      </Card>

      <Field className={styles.cardStyle}>
        <Button
          appearance="primary"
          name="submit"
          disabled={inputs.submitIsDisabled}
          size="large"
          onClick={handleSubmit}
        >
          Check Compatibility
        </Button>
      </Field>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px", width: "90%", marginBottom: "20px" }}>
        {infos.map((info) => (
          <MessageBar key={info["intent"]} layout="multiline" intent={info["intent"] as MessageBarIntent}>
            <MessageBarBody>
              <MessageBarTitle>Compatibility Info</MessageBarTitle>
              {info["info"]}
            </MessageBarBody>
            <MessageBarActions>
              <Button>Search on Web</Button>
            </MessageBarActions>
          </MessageBar>
        ))}
      </div>

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
              &nbsp;Formula Explanation
            </DialogTitle>
            <DialogContent>
              <Label className={styles.finst}></Label>
              {inputs.feedbackMsg}
            </DialogContent>

            <DialogActions>
              <Button
                appearance="primary"
                onClick={() => {
                  setFeedbackOpen(false);
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

export default CompChk;
