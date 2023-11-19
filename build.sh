# Build less.css files
for file in static/less/*; do
	lessc $file static/css/$(basename $file .less).css --source-map
done
