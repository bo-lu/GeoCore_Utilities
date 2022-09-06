# Collections API

## Test Cases

Usage: collections?id=$SOME_UUID

## Example case 1, no parameters provided: collections?

<pre>
{
  "statusCode": 200,
  "body": "No id parameter was passed. Usage: ?id=XYZ" 
}
</pre>

## Example case 2, searching for a non-existing record: collections?id=ASDF


<pre>
{
  "statusCode": 200,
  "sibling_count": 0,
  "self": null,
  "parent": null,
  "sibling": null
}
</pre>

## Example case 3, searching for a child record: collections?id=9cad712a-5ac5-4248-b7d7-2db1a3892509

<pre>
{
  "statusCode": 200,
  "sibling_count": 2,
  "self": {
    "id": "9cad712a-5ac5-4248-b7d7-2db1a3892509",
    "description_en": "Active Floods in Canada",
    "description_fr": "Inondations en cours au Canada" 
  },
  "parent": {
    "id": "08b810c2-7c81-40f1-adb1-c32c8a2c9f50",
    "description_en": "Floods in Canada - Cartographic Product Collection",
    "description_fr": "Inondations au Canada - collections de produits cartographiques" 
  },
  "sibling": [
    {
      "id": "74144824-206e-4cea-9fb9-72925a128189",
      "description_en": "Floods in Canada - Archive",
      "description_fr": "Inondations au Canada – Archive" 
    },
    {
      "id": "b1afd8d2-6e14-4ec4-9a09-652221a6cb71",
      "description_en": "Floods in Canada - Current Year",
      "description_fr": "Inondations au Canada – Année courante" 
    }
  ]
}
</pre>

## Example case 4, searching for a parent record: collections?id=08b810c2-7c81-40f1-adb1-c32c8a2c9f50

<pre>
{
  "statusCode": 200,
  "sibling_count": 3,
  "self": {
    "id": "08b810c2-7c81-40f1-adb1-c32c8a2c9f50",
    "description_en": "Floods in Canada - Cartographic Product Collection",
    "description_fr": "Inondations au Canada - collections de produits cartographiques" 
  },
  "parent": null,
  "sibling": [
    {
      "id": "74144824-206e-4cea-9fb9-72925a128189",
      "description_en": "Floods in Canada - Archive",
      "description_fr": "Inondations au Canada – Archive" 
    },
    {
      "id": "9cad712a-5ac5-4248-b7d7-2db1a3892509",
      "description_en": "Active Floods in Canada",
      "description_fr": "Inondations en cours au Canada" 
    },
    {
      "id": "b1afd8d2-6e14-4ec4-9a09-652221a6cb71",
      "description_en": "Floods in Canada - Current Year",
      "description_fr": "Inondations au Canada – Année courante" 
    }
  ]
}
</pre>

## Example case 5, searching for a record without sibling or parent: collections?id=2bcf34b5-4e9a-431b-9e43-1eace6c873bd

<pre>
{
  "statusCode": 200,
  "sibling_count": 0,
  "self": {
    "id": "2bcf34b5-4e9a-431b-9e43-1eace6c873bd",
    "description_en": "Inuit Communities Location",
    "description_fr": "Localisation des communautés inuites" 
  },
  "parent": null,
  "sibling": null
}
</pre>
