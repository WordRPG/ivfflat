#
# Adds a node package and links the project folder.
#
echo "--- INSTALLING PACKAGES"
npm install $@

echo "--- LINKING PROJECT FOLDER"
ln -s ../ node_modules/\$

echo "--- DONE."