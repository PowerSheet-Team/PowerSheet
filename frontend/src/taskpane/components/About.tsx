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

const About: React.FC = () => {
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
          <BreadcrumbButton icon={<BookToolboxRegular />}>About Us</BreadcrumbButton>
        </BreadcrumbItem>
      </Breadcrumb>
      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>About this project</b>
            </Body1>
          }
        />
        <Label>
          PowerSheet was developed for the &quot;2023 AMD Pervasive AI Developer Contest.&quot; This plugin harnesses
          the full capabilities of AMD Ryzen AI, offering functionalities such as content generation and data
          comprehension to enhance spreadsheet processing workflows locally, without uploading sensitive data to the
          cloud.
        </Label>
      </Card>

      <Card className={styles.cardStyle}>
        <CardHeader
          header={
            <Body1>
              <b>The authors</b>
            </Body1>
          }
        />
        <Label>
          You can find the authors at GitHub: <Link href="https://github.com/ftyghome">GnSight</Link> and{" "}
          <Link href="https://github.com/colorswind">ColorsWind</Link>.
        </Label>
      </Card>

      <Label>
        <RibbonStarFilled />
        <b>AMD, Yes!</b>
      </Label>
    </div>
  );
};

export default About;
