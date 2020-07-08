def get_followers():

    grab_info = (
        'at "full" range' if grab == "full" else "at the range of " "{}".format(grab)
    )
    tense = (
        "live"
        if (live_match is True or not relationship_data[username]["all_followers"])
        else "fresh"
    )

    user_link = "https://www.instagram.com/{}/".format(username)
    web_address_navigator(browser, user_link)

    # Get followers count
    grab, _ = get_relationship_counts(browser, username, logger)

    # sets the amount of usernames to be matched in the next queries

    user_data = {}
    graphql_endpoint = 
    graphql_followers = "view-source:https://www.instagram.com/graphql" "/query/?query_hash=37479f2b8209594dde7facb0d904896a"

    all_followers = []
    variables = {}
    try:
        user_data["id"] = browser.execute_script(
            "return window.__additionalData[Object.keys(window.__additionalData)[0]].data."
            "graphql.user.id"
        )
    except WebDriverException:
        user_data["id"] = browser.execute_script(
            "return window._sharedData." "entry_data.ProfilePage[0]." "graphql.user.id"
        )

    variables["id"] = user_data["id"]
    variables["first"] = 50

    # get follower and user loop

    sc_rolled = 0
    grab_notifier = False
    local_read_failure = False
    passed_time = "time loop"

    try:
        has_next_data = True

        url = "{}&variables={}".format(graphql_followers, str(json.dumps(variables)))
        web_address_navigator(browser, url)

        # Get stored graphql queries data to be used
        try:
            filename = "{}graphql_queries.json".format(logfolder)
            query_date = datetime.today().strftime("%d-%m-%Y")

            if not os.path.isfile(filename):
                with interruption_handler():
                    with open(filename, "w") as graphql_queries_file:
                        json.dump(
                            {username: {query_date: {"sc_rolled": 0}}},
                            graphql_queries_file,
                        )
                        graphql_queries_file.close()

            # load the existing graphql queries data
            with open(filename) as graphql_queries_file:
                graphql_queries = json.load(graphql_queries_file)
                stored_usernames = list(name for name, date in graphql_queries.items())

                if username not in stored_usernames:
                    graphql_queries[username] = {query_date: {"sc_rolled": 0}}
                stored_query_dates = list(
                    date for date, score in graphql_queries[username].items()
                )

                if query_date not in stored_query_dates:
                    graphql_queries[username][query_date] = {"sc_rolled": 0}
        except Exception as exc:
            logger.info(
                "Error occurred while getting `scroll` data from "
                "graphql_queries.json\n{}\n".format(str(exc).encode("utf-8"))
            )
            local_read_failure = True

        start_time = time.time()
        highest_value = followers_count if grab == "full" else grab
        # fetch all user while still has data
        while has_next_data:
            try:
                pre = browser.find_element_by_tag_name("pre").text
            except NoSuchElementException as exc:
                logger.info(
                    "Encountered an error to find `pre` in page!"
                    "\t~grabbed {} usernames \n\t{}".format(
                        len(set(all_followers)), str(exc).encode("utf-8")
                    )
                )
                return all_followers

            data = json.loads(pre)["data"]

            # get followers
            page_info = data["user"]["edge_followed_by"]["page_info"]
            edges = data["user"]["edge_followed_by"]["edges"]
            for user in edges:
                all_followers.append(user["node"]["username"])

            grabbed = len(set(all_followers))

            # write & update records at Progress Tracker
            progress_tracker(grabbed, highest_value, start_time, logger)

            finish_time = time.time()
            diff_time = finish_time - start_time
            diff_n, diff_s = (
                (diff_time / 60 / 60, "hours")
                if diff_time / 60 / 60 >= 1
                else (diff_time / 60, "minutes")
                if diff_time / 60 >= 1
                else (diff_time, "seconds")
            )
            diff_n = truncate_float(diff_n, 2)
            passed_time = "{} {}".format(diff_n, diff_s)

            if match is not None:
                matched_followers = len(set(all_followers)) - len(
                    set(all_followers) - set(all_prior_followers)
                )
                if matched_followers >= match:
                    new_followers = set(all_followers) - set(all_prior_followers)
                    all_followers = all_followers + all_prior_followers
                    print("\n")
                    logger.info(
                        "Grabbed {} new usernames from `Followers` in {}  "
                        "~total of {} usernames".format(
                            len(set(new_followers)),
                            passed_time,
                            len(set(all_followers)),
                        )
                    )
                    grab_notifier = True
                    break

            if grab != "full" and grabbed >= grab:
                print("\n")
                logger.info(
                    "Grabbed {} usernames from `Followers` as requested at {}".format(
                        grabbed, passed_time
                    )
                )
                grab_notifier = True
                break

            has_next_data = page_info["has_next_page"]
            if has_next_data:
                variables["after"] = page_info["end_cursor"]

                url = "{}&variables={}".format(
                    graphql_followers, str(json.dumps(variables))
                )

                web_address_navigator(browser, url)
                sc_rolled += 1

                # dump the current graphql queries data
                if local_read_failure is not True:
                    try:
                        with interruption_handler():
                            with open(filename, "w") as graphql_queries_file:
                                graphql_queries[username][query_date]["sc_rolled"] += 1
                                json.dump(graphql_queries, graphql_queries_file)
                    except Exception as exc:
                        print("\n")
                        logger.info(
                            "Error occurred while writing `scroll` data to "
                            "graphql_queries.json\n{}\n".format(
                                str(exc).encode("utf-8")
                            )
                        )

                # take breaks gradually
                if sc_rolled > 91:
                    print("\n")
                    logger.info("Queried too much! ~ sleeping a bit :>")
                    sleep(600)
                    sc_rolled = 0

    except BaseException as exc:
        print("\n")
        logger.info(
            "Unable to get `Followers` data:\n\t{}\n".format(str(exc).encode("utf-8"))
        )

    # remove possible duplicates
    all_followers = sorted(set(all_followers), key=lambda x: all_followers.index(x))

    if grab_notifier is False:
        print("\n")
        logger.info(
            "Grabbed {} usernames from `Followers` in {}".format(
                len(all_followers), passed_time
            )
        )

    if len(all_followers) > 0:
        if (
            store_locally is True
            and relationship_data[username]["all_followers"] != all_followers
        ):
            store_followers_data(username, grab, all_followers, logger, logfolder)
        elif store_locally is True:
            print("")
            logger.info(
                "The `Followers` data is identical with the data in previous "
                "query  ~not storing the file again"
            )

        if grab == "full":
            relationship_data[username].update({"all_followers": all_followers})

    sleep_t = sc_rolled * 6
    sleep_t = sleep_t if sleep_t < 600 else random.randint(585, 655)
    sleep_n, sleep_s = (
        (sleep_t / 60, "minutes") if sleep_t / 60 >= 1 else (sleep_t, "seconds")
    )
    sleep_n = truncate_float(sleep_n, 4)

    print("")
    logger.info(
        "Zz :[ time to take a good nap  ~sleeping {} {}".format(sleep_n, sleep_s)
    )
    sleep(sleep_t)
    logger.info("Yawn :] let's go!\n")

    return all_followers