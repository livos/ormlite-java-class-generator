import string
from helpers.ClassCreationHelper import getJavaType

class JavaClass: 

    def __init__(self, name, columns, packageName):
        self.name = name
        self.fields = columns
        self.packageName = packageName

    @property
    def packageName(self):
        return self._packageName

    @packageName.setter
    def packageName(self, value):
        self._packageName = value 

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value 

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, value):
        self._fields = value 

    def createJavaFile(self):
        INDENT = "    "
        IMPORT_FIELD = "import com.j256.ormlite.field.DatabaseField;\n"
        IMPORT_TABLE = "import com.j256.ormlite.table.DatabaseTable;\n"
        IMPORT_SERIALIZABLE = "import java.io.Serializable;\n\n"
        JAVA_CLASS_ANNOTATION = "@DatabaseTable(tableName = %sModel.TABLE_NAME_%s, daoClass = %sDao.class)\n"
        JAVA_CLASS = "public class %sModel implements Serializable {\n"
        JAVA_CLASS_TABLE_NAME = INDENT + "static final String TABLE_NAME_%s = \"%s\";\n";
        JAVA_CLASS_FIELD_CONST_DECLARATION_PKEY = INDENT + "static final String FIELD_%s_%s = \"%s\";\n"
        JAVA_CLASS_FIELD_CONST_DECLARATION = INDENT + "static final String FIELD_%s_%s = \"%s\";\n"
        JAVA_CLASS_FIELD_PKEY_ANNOTATION = INDENT + "@DatabaseField(generatedId = true, columnName = FIELD_%s_%s)\n"
        JAVA_CLASS_FIELD_ANNOTATION = INDENT + "@DatabaseField(columnName = FIELD_%s_%s)\n"
        JAVA_CLASS_FIELD_DECLARATION = INDENT + "private %s %s;\n"
        DEFAULT_CONSTRUCTOR = "\n" + INDENT + "public %sModel() { }\n"
        CONSTRUCTOR = "\n" + INDENT + "public %sModel%s " + INDENT + "\n"
        CONSTRUCTOR_AFFECTATION = INDENT + INDENT + "this.%s = %s;\n"
        GETTER = INDENT + "public %s get%s() { return %s; }\n\n"
        SETTER = INDENT + "public void set%s(%s %s) { this.%s = %s; }\n\n"


        fileName = self.name + "Model.java"

        print "Processing file %s" % fileName        

        with open(fileName, 'w+') as file:
            file.write("package %s\n\n" % self.packageName)
            file.write(IMPORT_TABLE)
            file.write(IMPORT_FIELD)
            file.write(IMPORT_SERIALIZABLE)
            file.write(JAVA_CLASS_ANNOTATION % (self.name, self.name.upper(),self.name))
            file.write(JAVA_CLASS % (self.name))
            file.write(JAVA_CLASS_TABLE_NAME % (self.name.upper(),self.name[:1].lower() + self.name[1:]))

            for field in self.fields:
                 if(field.isPrimaryKey):
                    file.write(JAVA_CLASS_FIELD_CONST_DECLARATION_PKEY % (self.name.upper(),field.name.upper(),field.name))
                 else:
                    file.write(JAVA_CLASS_FIELD_CONST_DECLARATION % (self.name.upper(),field.name.upper(),field.name))

            file.write("\n")

            for field in self.fields:
                if(field.isPrimaryKey):
                    file.write(JAVA_CLASS_FIELD_PKEY_ANNOTATION % (self.name.upper(), field.name.upper()))
                else:
                    file.write(JAVA_CLASS_FIELD_ANNOTATION % (self.name.upper(), field.name.upper()))
                
                file.write(JAVA_CLASS_FIELD_DECLARATION % (getJavaType(field.type),field.name))

            file.write(DEFAULT_CONSTRUCTOR % (self.name))

            constructorParams = "("
            for field in self.fields:
                constructorParams = "%s%s %s," % (constructorParams, getJavaType(field.type), field.name)
            constructorParams = constructorParams[:-1] + ") {"
            file.write(CONSTRUCTOR % (self.name,constructorParams))

            for field in self.fields:
                file.write(CONSTRUCTOR_AFFECTATION % (field.name,field.name))
            file.write(INDENT + "}\n\n")

            for field in self.fields:
                capitalizedField = field.name[:1].upper() + field.name[1:]
                file.write(GETTER % (getJavaType(field.type), capitalizedField, field.name))
                file.write(SETTER % (capitalizedField,getJavaType(field.type), field.name, field.name, field.name))

            file.write("}")