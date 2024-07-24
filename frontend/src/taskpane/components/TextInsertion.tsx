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
} from "@fluentui/react-components";
import {
  CalendarMonthFilled,
  CalendarMonthRegular,
  bundleIcon,
  BookToolboxRegular,
  RibbonStarFilled,
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
});

const TextInsertion: React.FC = () => {
  const connection = makeSocket();
  connection.on("message", function (msg) {
    recvRangeCandidate(msg);
    setOpen(false);
  });
  console.log(connection);

  const [inputs, setInputs] = useState({
    inputRange: "(No Selected)",
    outputRange: "(No Selected)",
    description: "",
    feedbackMsg: "",
    submitIsDisabled: false,
    loadingIsHidden: true,
  });

  const [open, setOpen] = React.useState(false);
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
      type: "fill",
      inputRange: inputs.inputRange,
      outputRange: inputs.outputRange,
      description: inputs.description,
      feedbackMsg: inputs.feedbackMsg,
      inputData: await getRangeData(inputs.inputRange),
      outputData: await getRangeData(inputs.outputRange),
    };
    connection.emit("message", msg);
    setOpen(true);

    console.log("submitted!", msg);
  };

  const handleFeedback = async () => {
    var msg = {
      type: "feedback",
      feedbackMsg: inputs.feedbackMsg,
    };
    connection.emit("message", msg);
    await promptForAddressRange();
    console.log("submitted!", msg);
  };

  const styles = useStyles();

  return (
    <div className={styles.textPromptAndInsertion}>
      <Breadcrumb aria-label="Breadcrumb default example">
        <BreadcrumbItem>
          <BreadcrumbButton icon={<BookToolboxRegular />}>Fill Content</BreadcrumbButton>
        </BreadcrumbItem>
      </Breadcrumb>
      {/* <MessageBar key="info" intent="info">
        <MessageBarBody>
          <MessageBarTitle>Info</MessageBarTitle>
          PowerSheet is powered by Ryzen AI. All your data are processed locally.
        </MessageBarBody>
      </MessageBar> */}
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Referencing Data</b>
            </Body1>
          }
          description={<Caption1>Select the data that should be referenced by the generated cell.</Caption1>}
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
              <b>Output Range</b>
            </Body1>
          }
          description={<Caption1>Select the output range that should be generated.</Caption1>}
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
          Fill Content
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
        open={open}
        onOpenChange={(_, data) => {
          // it is the users responsibility to react accordingly to the open state change
          setOpen(data.open);
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
    </div>
  );
};

export default TextInsertion;
