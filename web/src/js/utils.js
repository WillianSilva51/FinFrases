export const expirationMidnight = () => {
    const nextMidnight = new Date();
    nextMidnight.setDate(nextMidnight.getDate() + 1);
    nextMidnight.setUTCHours(0, 0, 0, 0);
    return nextMidnight.getTime();
};