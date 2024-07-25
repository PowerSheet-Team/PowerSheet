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

const AboutRyzen: React.FC = () => {
  const [inputs, setInputs] = useState({
    inputRange: "(No Selected)",
    outputRange: "(No Selected)",
    description: "",
    feedbackMsg: "",
    submitIsDisabled: false,
    loadingIsHidden: true,
  });

  const restoreFocusTargetAttribute = useRestoreFocusTarget();

  const styles = useStyles();

  return (
    <div className={styles.textPromptAndInsertion}>
      <Breadcrumb aria-label="Breadcrumb default example">
        <BreadcrumbItem>
          <BreadcrumbButton icon={<BookToolboxRegular />}>About Ryzen AI</BreadcrumbButton>
        </BreadcrumbItem>
      </Breadcrumb>
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>Overview</b>
            </Body1>
          }
        />
        <Label>
          AMD Ryzen AI is a feature integrated into AMD Ryzen processors that enhances performance in AI-driven
          applications. It leverages dedicated AI hardware to accelerate machine learning tasks, improving efficiency
          and enabling advanced capabilities in computing.
        </Label>
      </Card>

      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>PowerSheet and Ryzen AI</b>
            </Body1>
          }
        />
        <Label>
          PowerSheet is intended to run on a PC with Ryzen AI. While executing tasks for spreadsheet, AI models operate
          on the embedded NPU, freeing-up CPU and GPU resources for other compute tasks.
        </Label>
      </Card>

      <Label>
        <RibbonStarFilled />
        <b>AMD, Yes!</b>
      </Label>
    </div>
  );
};

export default AboutRyzen;
