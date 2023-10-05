var db = connect(`mongodb://${process.env.MONGO_INITDB_ROOT_USERNAME}:${process.env.MONGO_INITDB_ROOT_PASSWORD}@localhost:27017/admin`);

db = db.getSiblingDB(process.env.MONGO_INITDB_DATABASE);

db.createUser({
    user: process.env.MONGO_INITDB_USERNAME || 'jobsensei',
    pwd: process.env.MONGO_INITDB_PASSWORD || 'jobsensei',
    roles: [{
        role: 'readWrite', db: 'jobsensei',
    }],
});
