import * as React from "react";
import Header from "./Header";
import HeroList, { HeroListItem } from "./HeroList";
import TextInsertion from "./TextInsertion";
import About from "./About";
import AboutRyzen from "./AboutRyzen";
import DataSum from "./DataSum";
import FormulaExp from "./FormulaExp";
import { makeStyles, Label } from "@fluentui/react-components";
import { Ribbon24Regular, LockOpen24Regular, DesignIdeas24Regular } from "@fluentui/react-icons";
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
        </Switch>
      </Router>
    </div>
  );
};

export default App;
