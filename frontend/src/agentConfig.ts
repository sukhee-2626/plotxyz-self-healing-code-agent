export type FieldType = "text" | "textarea" | "number" | "checkbox";

export interface AgentField {
  name: string;
  label: string;
  type: FieldType;
  rows?: number;
  placeholder?: string;
}

export interface AgentConfig {
  slug: string;
  title: string;
  tagline: string;
  purpose: string;
  accent: string;
  features: string[];
  limitations: string[];
  fields: AgentField[];
  sample: Record<string, string | number | boolean>;
  repo: string;
}

export const agent: AgentConfig = {
  "slug": "plotxyz-self-healing-code-agent",
  "title": "Self-Healing Code",
  "tagline": "Patch the obvious problems before they become incidents.",
  "purpose": "Parses Python source, finds common defects such as bare excepts, None equality, mutable defaults, and dynamic execution, and generates syntax-validated patches.",
  "accent": "#f87171",
  "features": [
    "AST-based defect detection",
    "Syntax-validated safe patches",
    "Before/after patch preview"
  ],
  "limitations": [
    "Pattern-based fixes require human review.",
    "The agent never executes the supplied code."
  ],
  "fields": [
    {
      "name": "code",
      "label": "Python source",
      "type": "textarea",
      "rows": 10,
      "placeholder": ""
    }
  ],
  "sample": {
    "code": "def load(path):\n    try:\n        return open(path).read()\n    except:\n        return None\n\nif load(\"x\") == None:\n    print(\"missing\")"
  },
  "repo": "https://github.com/sukhee-2626/plotxyz-self-healing-code-agent"
};
