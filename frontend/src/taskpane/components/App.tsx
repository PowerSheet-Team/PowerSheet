import * as React from "react";
import TextInsertion from "./TextInsertion";
import About from "./About";
import AboutRyzen from "./AboutRyzen";
import DataSum from "./DataSum";
import FormulaExp from "./FormulaExp";
import FormulaPBE from "./FormulaPBE";
import RangeSel from "./RangeSel";
import BatchProc from "./BatchProc";
import CompChk from "./CompChk";
import Visual from "./Visual";
import { makeStyles } from "@fluentui/react-components";
import { HashRouter as Router, Switch, Route } from "react-router-dom";

interface AppProps {
  title: string;
}

const useStyles = makeStyles({
  root: {
    minHeight: "100vh",
  },
});

const App = (props: AppProps) => {
  const styles = useStyles();
  // The list items are static and won't change at runtime,
  // so this should be an ordinary const, not a part of state.
  console.log("state:", props);
  var _ = props;
  return (
    <div className={styles.root}>
      <Router>
        <Switch>
          <Route exact path="/fill" component={TextInsertion} />
          <Route exact path="/datasum" component={DataSum} />
          <Route exact path="/about" component={About} />
          <Route exact path="/aboutryzen" component={AboutRyzen} />
          <Route exact path="/formulaexp" component={FormulaExp} />
          <Route exact path="/pbe" component={FormulaPBE} />
          <Route exact path="/rangesel" component={RangeSel} />
          <Route exact path="/batchprocess" component={BatchProc} />
          <Route exact path="/compcheck" component={CompChk} />
          <Route exact path="/createvisual" component={Visual} />
        </Switch>
      </Router>
    </div>
  );
};

export default App;
